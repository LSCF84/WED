import openai
import json
import os
from datetime import datetime

class AIService:
    def __init__(self, api_key=None):
        # Configurar API key de OpenAI
        self.api_key = api_key or os.getenv('OPENAI_API_KEY', '')
        
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("Advertencia: No se configuró API key de OpenAI. Usando análisis simulado.")
    
    def analyze_events(self, events):
        """Analizar eventos con IA"""
        if not self.api_key:
            return self._get_mock_analysis(events)
        
        try:
            prompt = self._build_analysis_prompt(events)
            
            # Usar el cliente de OpenAI más reciente
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """Eres un experto técnico en sistemas Windows. Analiza los logs de eventos y 
                        proporciona diagnóstico y soluciones en formato JSON estructurado. Responde en español.
                        Sé conciso pero informativo."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            analysis_text = response.choices[0].message.content
            return self._parse_ai_response(analysis_text)
            
        except Exception as e:
            print(f"Error en análisis con IA: {str(e)}")
            # Si hay error de API, usar análisis simulado
            return self._get_mock_analysis(events, True)
    
    def _get_mock_analysis(self, events, api_error=False):
        """Análisis simulado cuando no hay API key o hay error"""
        error_count = len(events)
        
        if api_error:
            errors = [
                'Error de conexión con OpenAI API',
                f'Se detectaron {error_count} eventos en el sistema',
                'Verifica tu API key y conexión a internet'
            ]
            solutions = [
                'Verificar que la API key sea correcta',
                'Comprobar conexión a internet',
                'Revisar el saldo de la cuenta de OpenAI'
            ]
            confidence = 0
            severity = "Desconocido"
        else:
            errors = [
                'Configuración: No se configuró API key de OpenAI',
                f'Se detectaron {error_count} eventos de error/advertencia en el sistema',
                'No se puede realizar análisis detallado sin configuración de IA'
            ]
            solutions = [
                'Configurar API key de OpenAI en la interfaz',
                'Obtener una API key desde https://platform.openai.com/api-keys',
                'Revisar manualmente los eventos en el Visor de Eventos de Windows'
            ]
            confidence = 0
            severity = "Requiere Configuración"
        
        return {
            'severity_level': severity,
            'confidence': confidence,
            'detected_errors': errors,
            'recommended_solutions': solutions,
            'automated_steps': [
                'Ejecutar comprobación de archivos del sistema (sfc /scannow)',
                'Ejecutar limpieza de archivos temporales',
                'Verificar actualizaciones de Windows'
            ]
        }
    
    def _build_analysis_prompt(self, events):
        """Construir prompt para análisis"""
        prompt = f"""Analiza los siguientes eventos de Windows y proporciona diagnóstico y soluciones en formato JSON.

Eventos a analizar ({len(events)} eventos):
{self._format_events_for_prompt(events)}

Proporciona la respuesta en formato JSON exactamente como este ejemplo:
{{
    "severity_level": "Alto|Medio|Bajo",
    "confidence": 85,
    "detected_errors": ["Error description 1", "Error description 2"],
    "recommended_solutions": ["Solution 1", "Solution 2"],
    "automated_steps": ["Step 1", "Step 2"]
}}

Responde ÚNICAMENTE con el JSON, sin texto adicional."""
        
        return prompt
    
    def _format_events_for_prompt(self, events):
        """Formatear eventos para el prompt"""
        formatted = []
        for i, event in enumerate(events[:8]):  # Limitar para no exceder tokens
            formatted.append(f"""
Evento #{i+1}:
- Log: {event['log_type']}
- ID: {event['event_id']}
- Tipo: {event['event_type']}
- Fecha: {event['time_generated']}
- Fuente: {event['source']}
- Mensaje: {event['message'][:300]}...
""")
        return "\n".join(formatted)
    
    def _parse_ai_response(self, response_text):
        """Parsear respuesta de IA"""
        try:
            # Intentar encontrar JSON en la respuesta
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                analysis = json.loads(json_str)
                
                # Validar estructura esperada
                required_fields = ['severity_level', 'confidence', 'detected_errors', 
                                 'recommended_solutions', 'automated_steps']
                
                for field in required_fields:
                    if field not in analysis:
                        if field == 'detected_errors':
                            analysis[field] = []
                        elif field == 'recommended_solutions':
                            analysis[field] = []
                        elif field == 'automated_steps':
                            analysis[field] = []
                        elif field == 'confidence':
                            analysis[field] = 0
                        elif field == 'severity_level':
                            analysis[field] = 'Desconocido'
                        
                return analysis
            else:
                raise ValueError("No se encontró JSON en la respuesta")
                
        except Exception as e:
            print(f"Error parseando respuesta de IA: {str(e)}")
            return self._get_mock_analysis([], True)
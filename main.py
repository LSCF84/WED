import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import customtkinter as ctk
from event_log_manager import EventLogManager
from ai_service import AIService
from system_fixer import SystemFixer
import json
import os

class WindowsErrorDiagnosticApp:
    def __init__(self):
        # Configurar apariencia
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("Diagnóstico de Windows con IA")
        self.root.geometry("950x750")
        
        self.event_log_manager = EventLogManager()
        self.system_fixer = SystemFixer()
        
        # Inicializar AI Service sin API key primero
        self.ai_service = AIService("")
        
        # Cargar configuración si existe
        self.config_file = "config.json"
        self.load_config()
        
        self.setup_ui()
        
    def load_config(self):
        """Cargar configuración desde archivo"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.api_key = config.get('openai_api_key', '')
            else:
                self.api_key = ''
        except:
            self.api_key = ''
    
    def save_config(self):
        """Guardar configuración en archivo"""
        try:
            config = {
                'openai_api_key': self.api_key
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
        
    def setup_ui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(
            main_frame, 
            text="Diagnóstico Inteligente de Windows",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Frame de configuración API
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", padx=10, pady=5)
        
        # Etiqueta y campo para API Key
        api_key_label = ctk.CTkLabel(
            config_frame,
            text="OpenAI API Key:",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        api_key_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        api_key_frame = ctk.CTkFrame(config_frame)
        api_key_frame.pack(fill="x", padx=10, pady=5)
        
        self.api_key_entry = ctk.CTkEntry(
            api_key_frame,
            placeholder_text="Ingresa tu API Key de OpenAI...",
            show="•",
            width=400
        )
        self.api_key_entry.pack(side="left", padx=(0, 10), pady=5, fill="x", expand=True)
        
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key)
        
        self.save_api_btn = ctk.CTkButton(
            api_key_frame,
            text="Guardar Key",
            command=self.save_api_key,
            width=100
        )
        self.save_api_btn.pack(side="right", pady=5)
        
        # Información sobre cómo obtener la API key
        info_label = ctk.CTkLabel(
            config_frame,
            text="• Obtén tu API key en: https://platform.openai.com/api-keys",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        info_label.pack(anchor="w", padx=10, pady=(0, 10))
        
        # Frame de botones
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        # Botón Analizar
        self.analyze_btn = ctk.CTkButton(
            button_frame,
            text="🔍 Analizar Sistema",
            command=self.analyze_system,
            width=150,
            height=35
        )
        self.analyze_btn.pack(side="left", padx=5)
        
        # Botón Reparar
        self.fix_btn = ctk.CTkButton(
            button_frame,
            text="🔧 Reparación Automática",
            command=self.fix_system,
            width=150,
            height=35,
            fg_color="#D9534F",
            hover_color="#C9302C"
        )
        self.fix_btn.pack(side="left", padx=5)
        
        # Botón Limpiar Resultados
        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Limpiar",
            command=self.clear_results,
            width=100,
            height=35,
            fg_color="#5BC0DE",
            hover_color="#31B0D5"
        )
        self.clear_btn.pack(side="right", padx=5)
        
        # Barra de progreso
        self.progress_bar = ctk.CTkProgressBar(main_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=5)
        self.progress_bar.set(0)
        
        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Listo para analizar" + (" (API Key configurada)" if self.api_key else " (Configura API Key primero)"),
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)
        
        # Indicador de estado de API Key
        self.api_status_label = ctk.CTkLabel(
            main_frame,
            text="✅ API Key Configurada" if self.api_key else "❌ API Key No Configurada",
            font=ctk.CTkFont(size=11),
            text_color="green" if self.api_key else "red"
        )
        self.api_status_label.pack(pady=2)
        
        # Área de resultados
        results_frame = ctk.CTkFrame(main_frame)
        results_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Texto de resultados con scroll
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#2B2B2B",
            fg="white",
            insertbackground="white"
        )
        self.results_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Configurar tags para formato de texto
        self.results_text.tag_configure("title", font=("Consolas", 12, "bold"), foreground="#4FC3F7")
        self.results_text.tag_configure("subtitle", font=("Consolas", 10, "bold"), foreground="#81C784")
        self.results_text.tag_configure("warning", foreground="#FFB74D")
        self.results_text.tag_configure("error", foreground="#E57373")
        self.results_text.tag_configure("success", foreground="#81C784")
        
    def save_api_key(self):
        """Guardar la API key ingresada por el usuario"""
        api_key = self.api_key_entry.get().strip()
        
        if not api_key:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una API Key válida.")
            return
        
        if len(api_key) < 20:
            messagebox.showwarning("Advertencia", "La API Key parece demasiado corta. Verifica que sea correcta.")
            return
        
        self.api_key = api_key
        self.ai_service = AIService(api_key)
        
        # Actualizar UI
        self.api_status_label.configure(
            text="✅ API Key Configurada", 
            text_color="green"
        )
        self.status_label.configure(text="API Key guardada correctamente")
        
        # Guardar en archivo de configuración
        self.save_config()
        
        messagebox.showinfo("Éxito", "API Key guardada correctamente.\nYa puedes usar el análisis con IA.")
        
    def analyze_system(self):
        """Iniciar análisis del sistema en un hilo separado"""
        if not self.api_key:
            messagebox.showwarning(
                "API Key Requerida", 
                "Para usar el análisis con IA, primero configura tu API Key de OpenAI.\n\n"
                "1. Ve a https://platform.openai.com/api-keys\n"
                "2. Crea una nueva API key\n"
                "3. Pégala en el campo de texto arriba\n"
                "4. Haz clic en 'Guardar Key'"
            )
            return
            
        self.analyze_btn.configure(state="disabled")
        self.fix_btn.configure(state="disabled")
        self.save_api_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Obteniendo eventos del sistema...")
        
        thread = threading.Thread(target=self._analyze_thread)
        thread.daemon = True
        thread.start()
        
    def _analyze_thread(self):
        """Hilo para el análisis del sistema"""
        try:
            # Actualizar UI desde el hilo principal
            self.root.after(0, self._update_progress, 0.1, "Obteniendo logs del sistema...")
            
            # Obtener eventos de error
            error_events = self.event_log_manager.get_recent_error_events()
            
            if not error_events:
                self.root.after(0, self._show_message, "✅ No se encontraron errores recientes en los logs del sistema.")
                return
            
            self.root.after(0, self._update_progress, 0.3, f"Encontrados {len(error_events)} eventos. Preparando análisis...")
            
            # Mostrar eventos encontrados
            events_preview = f"Se encontraron {len(error_events)} eventos de error/aviso:\n\n"
            for i, event in enumerate(error_events[:5]):  # Mostrar solo primeros 5
                events_preview += f"Evento {i+1}: {event['source']} (ID: {event['event_id']})\n"
            
            self.root.after(0, self._update_progress, 0.5, "Conectando con IA para análisis...")
            
            # Analizar con IA
            analysis = self.ai_service.analyze_events(error_events)
            
            self.root.after(0, self._update_progress, 0.8, "Generando reporte...")
            self.root.after(0, self._display_analysis, analysis, error_events)
            self.root.after(0, self._update_progress, 1.0, "Análisis completado")
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Error durante el análisis: {str(e)}")
        finally:
            self.root.after(0, self._enable_buttons)
            
    def fix_system(self):
        """Iniciar reparación del sistema en un hilo separado"""
        self.analyze_btn.configure(state="disabled")
        self.fix_btn.configure(state="disabled")
        self.save_api_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_label.configure(text="Iniciando reparación automática...")
        
        thread = threading.Thread(target=self._fix_thread)
        thread.daemon = True
        thread.start()
        
    def _fix_thread(self):
        """Hilo para la reparación del sistema"""
        try:
            self.root.after(0, self._update_progress, 0.1, "Limpiando archivos temporales...")
            self.system_fixer.clean_temp_files()
            
            self.root.after(0, self._update_progress, 0.3, "Ejecutando comprobación de archivos del sistema...")
            self.system_fixer.run_system_file_checker()
            
            self.root.after(0, self._update_progress, 0.6, "Ejecutando DISM...")
            self.system_fixer.run_dism()
            
            self.root.after(0, self._update_progress, 0.9, "Finalizando...")
            self.root.after(0, self._update_progress, 1.0, "Reparación completada")
            
            self.root.after(0, lambda: messagebox.showinfo(
                "Completado", 
                "✅ Procedimientos automáticos ejecutados correctamente.\n\n"
                "Algunas correcciones pueden requerir reinicio del sistema."
            ))
            
        except Exception as e:
            self.root.after(0, self._show_error, f"Error durante la reparación: {str(e)}")
        finally:
            self.root.after(0, self._enable_buttons)
            
    def clear_results(self):
        """Limpiar el área de resultados"""
        self.results_text.delete(1.0, tk.END)
        self.status_label.configure(text="Resultados limpiados")
            
    def _update_progress(self, value, status):
        """Actualizar barra de progreso y estado"""
        self.progress_bar.set(value)
        self.status_label.configure(text=status)
        
    def _display_analysis(self, analysis, error_events):
        """Mostrar resultados del análisis"""
        text_widget = self.results_text
        text_widget.delete(1.0, tk.END)
        
        text_widget.insert(tk.END, "ANÁLISIS DEL SISTEMA CON IA\n", "title")
        text_widget.insert(tk.END, "=" * 50 + "\n\n")
        
        # Información de eventos encontrados
        text_widget.insert(tk.END, f"Eventos analizados: {len(error_events)}\n", "subtitle")
        text_widget.insert(tk.END, f"Nivel de Criticidad: ", "subtitle")
        
        # Color según nivel de criticidad
        severity = analysis['severity_level'].lower()
        if 'alto' in severity or 'crítico' in severity:
            text_widget.insert(tk.END, f"{analysis['severity_level']}\n", "error")
        elif 'medio' in severity:
            text_widget.insert(tk.END, f"{analysis['severity_level']}\n", "warning")
        else:
            text_widget.insert(tk.END, f"{analysis['severity_level']}\n", "success")
            
        text_widget.insert(tk.END, f"Confianza del análisis: {analysis['confidence']}%\n\n")
        
        text_widget.insert(tk.END, "🔍 ERRORES DETECTADOS:\n", "subtitle")
        text_widget.insert(tk.END, "-" * 20 + "\n")
        for error in analysis['detected_errors']:
            text_widget.insert(tk.END, f"• {error}\n")
        
        text_widget.insert(tk.END, "\n💡 SOLUCIONES RECOMENDADAS:\n", "subtitle")
        text_widget.insert(tk.END, "-" * 25 + "\n")
        for solution in analysis['recommended_solutions']:
            text_widget.insert(tk.END, f"• {solution}\n")
        
        text_widget.insert(tk.END, "\n⚙️ PASOS AUTOMÁTICOS DISPONIBLES:\n", "subtitle")
        text_widget.insert(tk.END, "-" * 30 + "\n")
        for step in analysis['automated_steps']:
            text_widget.insert(tk.END, f"• {step}\n")
            
        # Agregar recomendación final
        text_widget.insert(tk.END, "\n" + "=" * 50 + "\n", "title")
        text_widget.insert(tk.END, "💡 Recomendación: ", "subtitle")
        if 'alto' in severity or 'crítico' in severity:
            text_widget.insert(tk.END, "Se recomienda acción inmediata. Usa 'Reparación Automática' o sigue las soluciones manuales.\n", "error")
        else:
            text_widget.insert(tk.END, "Puedes usar 'Reparación Automática' para resolver problemas comunes.\n", "success")
        
    def _show_message(self, message):
        """Mostrar mensaje en el área de resultados"""
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, message, "success")
        
    def _show_error(self, error_message):
        """Mostrar mensaje de error"""
        messagebox.showerror("Error", error_message)
        self.status_label.configure(text="Error durante el análisis")
        
    def _enable_buttons(self):
        """Habilitar botones nuevamente"""
        self.analyze_btn.configure(state="normal")
        self.fix_btn.configure(state="normal")
        self.save_api_btn.configure(state="normal")
        
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

if __name__ == "__main__":
    app = WindowsErrorDiagnosticApp()
    app.run()
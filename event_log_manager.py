import win32evtlog
import win32con
from datetime import datetime, timedelta
import pythoncom

class EventLogManager:
    def __init__(self):
        self.server = "localhost"  # Servidor local
        self.log_types = ["System", "Application"]
        
    def get_recent_error_events(self, hours_back=24, max_events=50):
        """Obtener eventos de error recientes"""
        error_events = []
        
        for log_type in self.log_types:
            try:
                # Inicializar COM para este hilo
                pythoncom.CoInitialize()
                
                hand = win32evtlog.OpenEventLog(self.server, log_type)
                flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
                
                events = []
                while True:
                    events_batch = win32evtlog.ReadEventLog(hand, flags, 0)
                    if not events_batch:
                        break
                    
                    for event in events_batch:
                        # Filtrar por tipo de evento (Error o Advertencia) y tiempo
                        if (event.EventType in [win32con.EVENTLOG_ERROR_TYPE, win32con.EVENTLOG_WARNING_TYPE] and
                            self._is_recent_event(event.TimeGenerated, hours_back)):
                            
                            event_data = {
                                'log_type': log_type,
                                'event_id': event.EventID,
                                'event_type': self._get_event_type_name(event.EventType),
                                'time_generated': event.TimeGenerated,
                                'source': event.SourceName,
                                'message': self._get_event_message(event)
                            }
                            events.append(event_data)
                    
                    if len(events) >= max_events:
                        break
                
                error_events.extend(events[:max_events])
                win32evtlog.CloseEventLog(hand)
                
            except Exception as e:
                print(f"Error accediendo al log {log_type}: {str(e)}")
            finally:
                pythoncom.CoUninitialize()
        
        return error_events[:max_events]
    
    def _is_recent_event(self, event_time, hours_back):
        """Verificar si el evento es reciente"""
        if isinstance(event_time, datetime):
            time_diff = datetime.now() - event_time
            return time_diff <= timedelta(hours=hours_back)
        return True
    
    def _get_event_type_name(self, event_type):
        """Obtener nombre legible del tipo de evento"""
        event_types = {
            win32con.EVENTLOG_ERROR_TYPE: "Error",
            win32con.EVENTLOG_WARNING_TYPE: "Advertencia",
            win32con.EVENTLOG_INFORMATION_TYPE: "Información"
        }
        return event_types.get(event_type, "Desconocido")
    
    def _get_event_message(self, event):
        """Obtener mensaje del evento"""
        try:
            if event.StringInserts:
                return " ".join(str(insert) for insert in event.StringInserts if insert)
            return "No message available"
        except:
            return "Error reading message"
    
    def format_events_for_analysis(self, events):
        """Formatear eventos para análisis"""
        formatted = []
        for event in events:
            formatted.append(
                f"Log: {event['log_type']}\n"
                f"ID: {event['event_id']}\n"
                f"Tipo: {event['event_type']}\n"
                f"Fecha: {event['time_generated']}\n"
                f"Fuente: {event['source']}\n"
                f"Mensaje: {event['message'][:500]}...\n"
                f"{'-'*50}\n"
            )
        return "\n".join(formatted)
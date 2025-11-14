import subprocess
import os
import tempfile
import shutil

class SystemFixer:
    def __init__(self):
        self.temp_paths = [
            tempfile.gettempdir(),
            os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Temp'),
            os.environ.get('TEMP', ''),
            os.environ.get('TMP', '')
        ]
    
    def clean_temp_files(self):
        """Limpiar archivos temporales"""
        print("Limpiando archivos temporales...")
        for temp_path in self.temp_paths:
            if os.path.exists(temp_path):
                try:
                    for root, dirs, files in os.walk(temp_path):
                        for file in files:
                            try:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                                print(f"Eliminado: {file_path}")
                            except (PermissionError, OSError):
                                # Ignorar archivos en uso o sin permisos
                                pass
                except Exception as e:
                    print(f"Error limpiando {temp_path}: {str(e)}")
    
    def run_system_file_checker(self):
        """Ejecutar comprobador de archivos del sistema"""
        print("Ejecutando SFC /scannow...")
        try:
            result = subprocess.run(
                ['sfc', '/scannow'],
                capture_output=True,
                text=True,
                timeout=600  # 10 minutos máximo
            )
            print(f"SFC completado: {result.returncode}")
            print(f"Salida: {result.stdout}")
        except subprocess.TimeoutExpired:
            print("SFC timeout - proceso tomó demasiado tiempo")
        except Exception as e:
            print(f"Error ejecutando SFC: {str(e)}")
    
    def run_dism(self):
        """Ejecutar DISM para reparar imagen del sistema"""
        print("Ejecutando DISM...")
        try:
            # Primero verificar la imagen
            check_result = subprocess.run(
                ['DISM', '/Online', '/Cleanup-Image', '/CheckHealth'],
                capture_output=True,
                text=True,
                timeout=300
            )
            print(f"DISM CheckHealth: {check_result.returncode}")
            
            # Luego reparar si es necesario
            if check_result.returncode != 0:
                repair_result = subprocess.run(
                    ['DISM', '/Online', '/Cleanup-Image', '/RestoreHealth'],
                    capture_output=True,
                    text=True,
                    timeout=600
                )
                print(f"DISM RestoreHealth: {repair_result.returncode}")
                
        except subprocess.TimeoutExpired:
            print("DISM timeout - proceso tomó demasiado tiempo")
        except Exception as e:
            print(f"Error ejecutando DISM: {str(e)}")
    
    def check_disk(self):
        """Verificar disco"""
        print("Programando verificación de disco...")
        try:
            result = subprocess.run(
                ['chkdsk', 'C:', '/f'],
                capture_output=True,
                text=True,
                timeout=30
            )
            print("Verificación de disco programada para el próximo reinicio")
        except Exception as e:
            print(f"Error programando chkdsk: {str(e)}")
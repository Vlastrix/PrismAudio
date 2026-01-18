import os
import subprocess
import shutil

def process_audio(file_path: str, output_dir: str):
    """
    Separa el archivo de audio usando Demucs (Facebook Research).
    Demucs genera 4 pistas por defecto: vocals, drums, bass, other.
    Combinaremos drums+bass+other para crear el 'instrumental'.
    """
    try:
        # Comando para ejecutar demucs
        # -n htdemucs: usa el modelo por defecto (alta calidad)
        # --two-stems=vocals: hace exactamente lo que queremos (vocals + resto)
        # -o output_dir: directorio de salida
        command = [
            "demucs",
            "-n", "htdemucs",
            "--two-stems", "vocals",
            "-o", output_dir,
            file_path
        ]
        
        print(f"Ejecutando Demucs: {' '.join(command)}")
        subprocess.run(command, check=True)
        
        # Demucs crea una estructura: output_dir/htdemucs/nombre_archivo/
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        model_name = "htdemucs"
        result_dir = os.path.join(output_dir, model_name, base_name)
        
        # Archivos generados
        vocals_path = os.path.join(result_dir, "vocals.wav")
        no_vocals_path = os.path.join(result_dir, "no_vocals.wav")
        
        # Para mantener compatibilidad con nuestro frontend, renombramos/movemos
        # Queremos: output_dir/nombre_archivo/vocals.wav y accompaniment.wav
        
        final_dir = os.path.join(output_dir, base_name)
        os.makedirs(final_dir, exist_ok=True)
        
        final_vocals = os.path.join(final_dir, "vocals.wav")
        final_acc = os.path.join(final_dir, "accompaniment.wav")
        
        if os.path.exists(vocals_path) and os.path.exists(no_vocals_path):
            shutil.copy2(vocals_path, final_vocals)
            shutil.copy2(no_vocals_path, final_acc)
            
            # Limpieza opcional de la carpeta de demucs si se desea
            # shutil.rmtree(os.path.join(output_dir, model_name))
            
            return {
                "success": True,
                "vocals": os.path.join(base_name, "vocals.wav"),
                "accompaniment": os.path.join(base_name, "accompaniment.wav"),
                "full_path": final_dir
            }
        else:
            return {"success": False, "error": "No files created by Demucs"}

    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Demucs: {e}")
        return {"success": False, "error": f"Demucs failed: {str(e)}"}
    except Exception as e:
        print(f"Error inesperado: {e}")
        return {"success": False, "error": str(e)}

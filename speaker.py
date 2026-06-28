import subprocess

class Speaker:

    def __init__(self):
        self.model = "/home/furank/Documentos/Proyectos/faper-trainer/voices/es_ES-sharvard-medium.onnx"

    def hablar(self, texto):

        proceso = subprocess.Popen(
            [
                "piper-tts",
                "--model", self.model,
                "--output_raw"
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE
        )

        audio, _ = proceso.communicate(input=texto.encode())

        subprocess.run([
            "aplay",
            "-f", "S16_LE",
            "-r", "22050",
            "-c", "1"
        ], input=audio)

from cx_Freeze import setup, Executable

setup(
    name = "OlimpTestConverter",
    version = "0.4",
    description = "vOlimpTestConverter",
    executables = [Executable("Course_gen.py")]
)
# python setup.py build
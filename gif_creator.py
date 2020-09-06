import imageio
import pathlib
import os, stat


def do(name):
    imageio.plugins.ffmpeg.download()
    p = pathlib.Path("source_images")
    names = list(p.glob("*.png"))
    mapper = dict()
    for el in names:
        mapper[el.name] = int(el.name[:-4])
    names = sorted(names, key=lambda x: mapper[x.name])
    result = []
    for n in names:
        result.append(imageio.imread(n))
    os.chdir("source_images")
    for file_name in os.listdir(os.getcwd()):
        try:
            os.remove(file_name)
        except PermissionError:
            os.chmod(file_name, stat.S_IWRITE)
            os.remove(file_name)
    os.chdir("..")
    os.chdir("examples")
    imageio.mimwrite(f"{name}.gif", result)
    os.chdir("..")

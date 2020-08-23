import imageio
import pathlib
import os,stat

def do(pos=1):
    imageio.plugins.ffmpeg.download()
    p = pathlib.Path("source_images")
    names = list(p.glob("*.png"))
    mapper = dict()
    for el in names:
        mapper[el.name] = int(el.name[:-4])
    names = sorted(names,key=lambda x:mapper[x.name])
    result = []
    for n in names:
        for i in range(6):
            result.append(imageio.imread(n))
    imageio.mimwrite(f"test{pos}.gif",result)
    os.chdir(p)
    for file_name in os.listdir(os.getcwd()):
        try:
            os.remove(file_name)
        except PermissionError:
            os.chmod(file_name, stat.S_IWRITE)
            os.remove(file_name)
    os.chdir("..")

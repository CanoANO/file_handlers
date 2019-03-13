from pathlib import Path
import os


def dig(indir, outdir, callback, file_format, args, restriction=''):
    """Dig into the indir and use callback to handle every file with given file_format.
    The first two parameter of callback must be indir and outdir, the rest of parameters is in args.
    Save the output into outdir and keep the same sub dir structure as indir.
    If the restriction is applied, all file with file_format whose name contains restriction will be handled.

    example:
    # segmentation.main takes three parameters: indir, outdir, [aggre, seg_length, csv]
    dig('./data', './out', segmentation.main, 'wav', [3, 0, True], '小V小V')

    :param indir: str
    :param outdir: str
    :param callback: function
    :param file_format: str
    :param args: list
    :param restriction: str
    :return: None
    """
    indir = Path(indir)
    outdir = Path(outdir)
    if not (indir.is_dir() and outdir.is_dir()):
        print('wrong dir path')
        exit(0)
    queue = [indir]
    while queue:
        curr = queue.pop()
        queue.extend([d for d in curr.iterdir() if d.is_dir()])
        todo = [f for f in curr.glob('*.' + file_format) if restriction in f.stem]
        curr_out = str(outdir) + (str(curr)[len(str(indir)):])
        if curr_out != str(outdir):
            os.mkdir(curr_out)
        for file in todo:
            callback(str(file), curr_out, args)
            print(file, 'is handled')


def rerange_name(path: Path, name_format, file_format):
    files = sorted(path.glob('*.' + file_format))
    names = [Path(str(path) + '/' + name_format % (i,)) for i in range(len(files))]
    for i in range(len(files)):
        os.rename(str(files[i]), str(names[i]))


def clean_filter(indir, lower_bound, upper_bound, name_format, file_format):
    """ Delete some files with given file_format in the indir directory whose size is below lower_bound or
    above upper_bound. Reformatting all file names with file_format into given name_format.

    :param indir: str
    :param lower_bound: int (represents in kb)
    :param upper_bound: int (represents in kb)
    :param name_format: str
    :param file_format: str
    :return: None
    """

    for f in Path(indir).iterdir():
        if f.is_dir():
            for file in f.glob('*.' + file_format):
                size = os.path.getsize(file)
                if size < lower_bound * 1024 or size > upper_bound * 1024:
                    os.remove(str(file))
                    print(file, 'removed')
            rerange_name(f, name_format, file_format)


if __name__ == '__main__':
    pass

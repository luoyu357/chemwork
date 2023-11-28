import subprocess

#brew install open-babel
import uuid


def convert_string_to_structure(smile_string, file_path):
    print(file_path)
    cmd = ["obabel", "-:"+smile_string, "-O", file_path]

    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)


# convert_string_to_structure('CN1C2=[C-]C(=CC=C2)N(C3=[C-]C(=CC=C3)OC4=CC=CC1=[C-]4)C.[Co+3]', '/Users/luoyu/PycharmProjects/chemwork/image/remake/TEST.png')
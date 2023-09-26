import subprocess

#brew install open-babel
import uuid


def convert_string_to_structure(smile_string, file_path):
    print(file_path)
    cmd = ["obabel", "-:"+smile_string, "-O", file_path]

    # Run the command
    result = subprocess.run(cmd, capture_output=True, text=True)


#convert_string_to_structure('CC1(C)c2cccc3c2[Co]2c4c1cccc4Oc1c2c(O3)ccc1', '/Users/luoyu/PycharmProjects/chemwork/image/remake/'+str(uuid.uuid4())+'.png')
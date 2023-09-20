import subprocess

def runOsraSmiles(inputPath, outputPath, outputName, inputName):
    subprocess.call(
        ['docker', 'container', 'run', '--rm', '--volume', inputPath + ':/input',
         '--volume', outputPath + ':/output',
         'daverona/osra', 'osra', '-c', '-p', '--write', '/output/' + outputName, '/input/' + inputName])
    f = open(outputPath + "/" + outputName, "r")
    return f.readlines()

# convert the OSRA output to machine-understandable values
def get_smiles(coordinates):
    output = []
    for items in coordinates:
        temp = []
        item = items.split(" ")
        temp.append(item[0])
        coordinate = item[2].replace("\n", '')
        coordinate = coordinate.split("x")

        x1 = coordinate[0]
        y2 = coordinate[2]
        y1x2 = coordinate[1].split("-")
        if len(y1x2) == 3:
            y1x2 = [y1x2[0] + y1x2[1], y1x2[2]]
        y1 = y1x2[0]
        x2 = y1x2[1]

        temp.append([int(x1), int(x2)])
        temp.append([int(y1), int(y2)])
        temp.append(float(item[1]))
        output.append(temp)
        # [['smiles', [x1,x2], [y1,y2], confidence], .... ]
        # ['c1cc2ccc3c4c2c(c1)c1cccc2c1[Co]4c1c(o3)cccc1o2', [0, 446], [0, 564], 3.1]
    return output


if __name__ == '__main__':
    result = runOsraSmiles(inputPath='/Users/luoyu/PycharmProjects/chemwork/image/in', outputPath='/Users/luoyu/PycharmProjects/chemwork/image/smiles', outputName='2.smi', inputName='2.png')
    print(get_smiles(result))
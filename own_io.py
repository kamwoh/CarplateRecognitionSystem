import os, cv2


def rename(file_path, new_file_path):
    os.rename(file_path, new_file_path)


def delete(file_path):
    os.remove(file_path)


def getFiles(folder_path, full_path=True):
    files = []
    for f in os.listdir(folder_path):
        path = os.path.join(folder_path, f)
        if os.path.isfile(path):
            if isImage(path):
                if full_path is False:
                    path = f
                files.append(path)
    return files


def getFolders(folder_path):
    folders = []
    for f in os.listdir(folder_path):
        path = os.path.join(folder_path, f)
        if os.path.isdir(path):
            folders.append(path)
    return folders


def getAllFiles(folder_path):
    files = []
    for f in os.listdir(folder_path):
        path = os.path.join(folder_path, f)
        if os.path.isfile(path):
            if isImage(path):
                files.append(path)
        else:
            temp = getAllFiles(path)
            for t in temp:
                files.append(t)
    return files


def isImage(file_path):
    if '.png' in file_path:
        return True
    elif '.jpg' in file_path:
        return True
    elif '.jpeg' in file_path:
        return True
    elif '.bmp' in file_path:
        return True
    else:
        return False


def readCv2Image(image_path, flags=None):
    if flags is None:
        return cv2.imread(image_path)
    else:
        return cv2.imread(image_path, flags)


def saveImage(image_path, cv2_img, params=None):
    cv2.imwrite(image_path, cv2_img, params)


def isExists(file_path):
    return os.path.exists(file_path)


def isFolder(folder_path):
    return os.path.isdir(folder_path)


def isFile(file_path):
    return not isFolder(file_path)


def correctFolderPath(folder_path):
    if isFolder(folder_path):
        if folder_path[-1] != '/':
            return folder_path+'/'
        else:
            return folder_path
    else:
        correctPath = dirName(folder_path)
        if correctPath[-1] != '/':
            correctPath += '/'
        return correctPath


def createDir(*folder_path):
    for path in folder_path:
        if not isExists(path):
            os.makedirs(path)

def getFullPath(file_path):
    return os.path.abspath(file_path)


def dirName(file_path):
    return os.path.dirname(file_path)


def fileName(file_path, withExtension=True):
    if withExtension:
        return os.path.basename(file_path)
    else:
        return os.path.splitext(os.path.basename(file_path))[0]

def join(folder_path,file_path):
    if folder_path[-1] == '/':
        return folder_path + file_path
    else:
        return folder_path + '/' + file_path

def folderName(folder_path):
    return os.path.basename(folder_path)


def extensionName(file_path):
    basename = fileName(file_path)
    split = os.path.splitext(basename)
    if len(split) == 1:
        return ''
    else:
        return split[-1]

def generateEmptyFolder(generate_path, total_number):
    createDir(generate_path)
    generate_path = correctFolderPath(generate_path)
    for i in xrange(total_number):
        createDir(generate_path+str(i))
        print 'generated folder:',generate_path+str(i)
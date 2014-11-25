import os


def create_filesystem(target_dir, parameters, data_provider_conf):
    conf = data_provider_conf['target']
    final_path = target_dir
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    if len(conf['folders']) > 0:
        for folder in conf['folders']:
            final_path = create_folder(conf, parameters, folder, target_dir)
    sub_folders = data_provider_conf['subfolders']
    bands = data_provider_conf['bands']
    for key in sub_folders:
        if 'output' in key:
            for band in bands:
                out_folder = os.path.join(final_path, sub_folders[key] + '_' + band['label'])
                if not os.path.exists(out_folder):
                    os.makedirs(out_folder)
        else:
            out_folder = os.path.join(final_path, sub_folders[key])
            if not os.path.exists(out_folder):
                os.makedirs(out_folder)

    return final_path


def create_folder(conf, parameters, folder, root_folder):
    folder_name = folder['folder_name']
    if '{{' in folder_name and '}}' in folder_name:
        for key in parameters:
            if str(folder['folder_name']) == '{{' + key + '}}':
                folder_name = str(folder['folder_name']).replace('{{' + key + '}}', str(parameters[key]))
    root_folder = os.path.join(root_folder, folder_name)
    if not os.path.exists(root_folder):
        os.makedirs(root_folder)
    if 'folders' in folder and len(folder['folders']) > 0:
        for sub_folder in folder['folders']:
            root_folder = create_folder(conf, parameters, sub_folder, root_folder)
    return root_folder
import os
import logging
import shutil


class BatchRenamer:
    def __init__(self, 
                 filepath          = None,
                 new_folder        = None,
                 copy_files        = False,
                 overwrite         = False,
                 filetypes         = None,
                 strings_to_find   = None,
                 string_to_replace = '',
                 prefix            = None,
                 suffix            = None):
        self.filepath          = filepath
        self.new_folder        = new_folder
        self.copy_files        = copy_files
        self.overwrite         = overwrite
        self.filetypes         = filetypes
        self.strings_to_find   = strings_to_find
        self.string_to_replace = string_to_replace
        self.prefix            = prefix
        self.suffix            = suffix

        self.initialize_logger()


    def initialize_logger(self, print_to_screen = True):
        """
        Creates a logger

        Args:
            print_to_screen: for printing to screen as well as file
        """

        ###############
        # Basic Setup #
        ###############
        app_title = 'batch_renamer_jinguang_huang'
        version_number = '1.0.1'
        # get the path the script was run from, storing with forward slashes
        source_path = os.path.dirname(os.path.realpath(__file__))
        # create a log filepath
        logfile_name = f'{app_title}.log'
        logfile = os.path.join(source_path, logfile_name)

        # tell the user where the log file is
        print(f'Logfile is {logfile}')

        # more initialization
        self.logger = logging.getLogger(f'{app_title} Logger')
        self.logger.setLevel(logging.INFO)
        
        ###############################
        # Formatter and Handler Setup #
        ###############################
        file_handler = logging.FileHandler(logfile)
        file_handler.setLevel(logging.INFO)
        # formatting information we want (time, self.logger name, version, etc.)
        formatter = logging.Formatter(f'%(asctime)s - %(name)s {version_number} - '
                                    '%(levelname)s - %(message)s')
        # setting the log file format
        file_handler.setFormatter(formatter)
        # clean up old handlers
        self.logger.handlers.clear()

        # add handler
        self.logger.addHandler(file_handler)

        # allowing to print to screen
        if print_to_screen:
            # create a new "stream handler" for logging/printing to screen
            console = logging.StreamHandler()
            self.logger.addHandler(console)
            # setting the print log format
            console.setFormatter(formatter)

        self.logger.info('Logger Initiated')


    def modify_file(self, existing_name, new_name,
                    new_folder, copy_mode, force):
        """
        Renames a file if it exists
        Only overwrites files if force is True

        Args:
            existing_name: full filepath a file that should already exist
            new_name: full filepath for new name
            copy_mode: copy instead of rename
            force: allows overwriting files
        """
        # Make sure existing_name is a file
        if os.path.isfile(existing_name):
            # Make sure new_name is not already a file
            if os.path.isfile(new_name):
                self.logger.error(f'{new_name} already exist!')
            else:
                if copy_mode:
                    shutil.copy(existing_name, new_name)
                    self.logger.info(f'copied {existing_name} to {new_name}')
                else:
                    # if it has new folder, copy the file directly
                    if new_folder:
                        shutil.copy(existing_name, new_name)
                        self.logger.info(f'copied {existing_name} to {new_name}')
                    else:
                        # if user don't provide new folder, check overwrite
                        if force:
                            shutil.move(existing_name, new_name)
                            self.logger.info(f'renamed {existing_name} to {new_name}')
                        # if not overwrite allowed, warning
                        else:
                            self.logger.warning("Don't override")
        else:
            # print("filepath is not a folder, please enter a valid folder")
            self.logger.error(f'{existing_name} does not exist!')


    def process_folder(self,
                       filepath,
                       new_folder,
                       copy_files,
                       overwrite,
                       filetypes,
                       strings_to_find,
                       string_to_replace,
                       prefix,
                       suffix):
        """
        Checks the given folder
        Gathers files in the folder
        Optionally limits files to modify
        Optionally does find and replace
        Optionally adds prefixes and suffixes

        Args:
            filepath: full filepath to a folder to find files in
            new_folder: full filepath to a folder to copy or move files to
            copy_mode: setting to copy files instead of rename them
            filetypes: filetypes to modify
            strings_to_find: list of strings to find in filename
            string_to_replace: string to replace and strings_to_find with
            prefix: string to add to the beginning of all modified files
            suffix: string to add to the end of all modified files
        """
        # check to see if the filepath is a valid folder
        if os.path.isdir(filepath):
            # check to see if new_folder is given
            if new_folder != "":
                # check to see if new_folder is exist
                if os.path.isdir(new_folder):
                    self.logger.info("new_folder is exist!")
                    # print("new_folder is exist!")
                    # print(new_folder)
                # make a new folder if it doesn't exist
                else:
                    # print("new_folder is given but it is not exist!")
                    # print("I will make it for you!")
                    self.logger.info("new_folder is given but it is not exist!")
                    self.logger.info("I will make it for you!")
                    os.makedirs(new_folder)
            else:
                self.logger.info("new_folder is not given!")
                self.logger.info("************************")
                pass
                # print("new_folder is not given!")

            # loop through all files inside the given filepath (folder)
            for filename in os.listdir(filepath):
                # get each file's extension if filetypes is given
                if strings_to_find:
                    if filetypes != "":
                        file_ext = os.path.splitext(filename)[1]
                        filename_old = os.path.splitext(filename)[0]
                        # print(f'File Extension : {file_ext}') #DEBUG
                        self.logger.info(f'File Extension : {file_ext}')
                        self.logger.info(f'Original File Name : {filename_old}')

                        # rename the file name
                        if file_ext == filetypes:

                            if strings_to_find in filename_old:
                                self.logger.info(f'string to find : {strings_to_find}')
                                self.logger.info("string to replace : ")
                                self.logger.info(f'{string_to_replace}')

                                if string_to_replace in filename_old:
                                    self.logger.info("filetypes, replace match!")
                                    self.logger.info("Strat the process!")

                                    name_new = filename_old.replace(
                                        filename_old,
                                        string_to_replace)
                                    if prefix != "":
                                        name_new = prefix + "_" + name_new
                                    else:
                                        self.logger.info("no prefix provide!")
                                        pass
                                    if suffix != "":
                                        name_new = name_new + "_" + suffix
                                    else:
                                        self.logger.info("no suffix provide!")
                                        pass

                                    # print(f'New File Name : {name_new}')
                                    self.logger.info(f'New File Name : {name_new}')

                                    # get each file's full path,
                                    # and reconstruct full path
                                    name_new = name_new + file_ext
                                    # check to see if we have new folder
                                    if new_folder:
                                        filename_fullpath = os.path.join(
                                            new_folder, name_new)
                                    else:
                                        filename_fullpath = os.path.join(
                                            filepath, name_new)
                                    # print(f'Filepath : {filename_fullpath}')
                                    target_path = filename_fullpath
                                    source_path = os.path.join(filepath,
                                                               filename)
                                    # print(f'Source Path : {source_path}')
                                    # print(f'Target Path : {target_path}')

                                    self.logger.info(f'Source Path : {source_path}')
                                    self.logger.info(f'Target Path : {target_path}')
                                    self.logger.info("************************")
                                    # source_path = target_path #for testing

                                    # final check to make sure target path
                                    # and source path are not the same
                                    if target_path != source_path:
                                        # call modify file fuction
                                        self.modify_file(source_path,
                                                         target_path,
                                                         new_folder,
                                                         copy_files,
                                                         overwrite)
                                    else:
                                        self.logger.warning(
                                            "target_path, source_path are same")
                                        self.logger.info("************************")
                                        self.modify_file(source_path,
                                                         target_path,
                                                         new_folder,
                                                         copy_files,
                                                         overwrite)
                                else:
                                    self.logger.info(
                                        "filename and replace name no match!")
                                    self.logger.info("************************")
                                    pass
                            else:
                                pass
                        else:
                            # print("filetypes doesn't match!")
                            # print("************************")
                            self.logger.info("filetypes doesn't match!")
                            self.logger.info("************************")
                            pass
                    else:
                        # print("Filetypes is not given!")
                        self.logger.info("Filetypes is not given!")
                        pass
                else:
                    # in the case that strings_to_find is empty
                    self.logger.info("Strings to find is empty!")
                    if filetypes != "":
                        file_ext = os.path.splitext(filename)[1]
                        filename_old = os.path.splitext(filename)[0]
                        # print(f'File Extension : {file_ext}') #DEBUG
                        self.logger.info(f'File Extension : {file_ext}')
                        self.logger.info(f'Original File Name : {filename_old}')

                        if file_ext == ".txt":
                            if prefix != "" and suffix != "":
                                name_new = prefix + "_" + filename_old
                                name_new = name_new + "_" + suffix

                                # print(f'New File Name : {name_new}')
                                self.logger.info(f'New File Name : {name_new}')

                                # get each file's full path, and rebuilt fullpath
                                name_new = name_new + file_ext
                                # check to see if we have new folder
                                if new_folder:
                                    filename_fullpath = os.path.join(new_folder,
                                                                     name_new)
                                else:
                                    filename_fullpath = os.path.join(filepath,
                                                                     name_new)
                                # print(f'Filepath : {filename_fullpath}')
                                target_path = filename_fullpath
                                source_path = os.path.join(filepath, filename)
                                # print(f'Source Path : {source_path}')
                                # print(f'Target Path : {target_path}')

                                self.logger.info(f'Source Path : {source_path}')
                                self.logger.info(f'Target Path : {target_path}')
                                self.logger.info("************************")
                                # source_path = target_path #for testing

                                # final check to make sure target path
                                # and source path are not the same
                                if target_path != source_path:
                                    # call modify file fuction
                                    self.modify_file(source_path,
                                                     target_path,
                                                     new_folder,
                                                     copy_files,
                                                     overwrite)
                                else:
                                    self.logger.warning(
                                        "target_path, source_path are same")
                                    self.logger.info("************************")
                                    pass
                            else:
                                self.logger.warning("no prefix or no suffix provide!")
                                self.logger.info("************************")
                                pass
                        else:
                            self.logger.info("do nothing!")
                            self.logger.info("************************")
                            pass
                    else:
                        # print("Filetypes is not given!")
                        self.logger.info("Filetypes is not given!")
                        pass
        else:
            # print("filepath is not a folder, please enter a valid folder")
            self.logger.error("filepath is not a folder, please enter a valid folder")

        #source_path = 'A FILEPATH YOU WILL CONSTRUCT'
        #target_path = 'A FILEPATH YOU WILL CONSTRUCT'

        #self.modify_file(logger, source_path, target_path, copy_mode=self.copy_files, force=self.overwrite)


if __name__ == '__main__':
    # This part will not be executed when importing
    testing_folder = r"D:\...\testing_files"
    # Create batch renamer object
    br = BatchRenamer(filepath=testing_folder)

    # Example usage for Models
    br.filetypes = '.ma'
    br.prefix = 'M_'
    br.strings_to_find = ['_file_01', '_file_final_new_02']
    br.process_folder()

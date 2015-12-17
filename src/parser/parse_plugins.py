import os
import json
import logging
import src.modules.plugin.plugin as class_plugin
import src.conf.settings.SETTINGS as SETTINGS


def parse_plugins():
    plugin_list = []

    for plugin_file in SETTINGS.PLUGINS_FILES:

        logging.info('processing source file: %s' % plugin_file)
        with open(os.path.join(SETTINGS.PLUGINS_DIR, plugin_file), 'r') as f:
            plugin_object = json.load(f)
        # f.close()

        plugin_dict = {}

        for release in plugin_object[u'releases']:
            logging.info('checking system for release: %s' % release[u'release_number'])

            if plugin_object[u'type'] == 'submitter':
                # architecture_fallback = None

                # if SETTINGS.ARCHITECTURE == 'x64' and release[u'architecture_fallback']:
                #     architecture_fallback = True
                # elif SETTINGS.ARCHITECTURE == 'x32':
                #     architecture_fallback = False

                label = str(plugin_object[u'vendor'] + ' ' +
                                plugin_object[u'family'] + ' ' +
                                release[u'release_number'])
                # label_x64 = str(plugin_object[u'vendor'] + ' ' +
                #                 plugin_object[u'family'] + ' ' +
                #                 release[u'release_number'] +
                #                 ' (%s)' % SETTINGS.ARCHITECTURES[SETTINGS.ARCHITECTURES.index('x64')])

                project_directories_list = []

                for project_directory in release[u'project_directories']:
                    project_directory = project_directory.replace('%', os.sep)
                    project_directories_list.append(project_directory)

                for platform_item in release[u'platforms']:
                    if SETTINGS.OPERATING_SYSTEM in platform_item:
                        executable = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable']
                        # executable_x64 = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable_x64']

                        executable_list = []

                        # for executable in [executable_x32, executable_x64]:
                        if executable is None:
                            logging.warning('executable is %s' % executable)
                        elif os.path.exists(executable):
                            executable_list.append(executable)
                            logging.info('executable %s found on this machine.' % executable)
                        elif not os.path.exists(executable):
                            logging.warning('executable %s not found on this machine.' % executable)

                        plugin_dict[u'family'] = \
                            plugin_object[u'family']
                        plugin_dict[u'type'] = \
                            plugin_object[u'type']
                        # plugin_dict[u'nodeable'] = \
                        #     plugin_object[u'nodeable']
                        # plugin_dict[u'node_only'] = \
                        #     plugin_object[u'node_only']
                        plugin_dict[u'family_enable'] = \
                            plugin_object[u'family_enable']
                        plugin_dict[u'vendor'] = \
                            plugin_object[u'vendor']
                        plugin_dict[u'abbreviation'] = \
                            plugin_object[u'abbreviation']
                        plugin_dict[u'release_number'] = \
                            release[u'release_number']
                        if release[u'icon'] is None:
                            plugin_dict[u'icon'] = release[u'icon']
                        else:
                            plugin_dict[u'icon'] = \
                                os.path.join(SETTINGS.PLUGINS_ICONS, release[u'icon'])
                        # plugin_dict[u'release_extension'] = \
                        #     release[u'release_extension']
                        # plugin_dict[u'project_template'] = \
                        #     release[u'project_template']
                        # plugin_dict[u'project_workspace_template'] = \
                        #     release[u'project_workspace_template']
                        plugin_dict[u'default_outputs'] = \
                            release[u'default_outputs']
                        # plugin_dict[u'architecture_fallback'] = \
                        #     architecture_fallback
                        plugin_dict[u'label'] = \
                            label
                        # plugin_dict[u'label_x64'] = \
                        #     label_x64
                        plugin_dict[u'project_directories'] = \
                            project_directories_list
                        plugin_dict[u'flags'] = \
                            platform_item[SETTINGS.OPERATING_SYSTEM][u'flags']
                        # plugin_dict[u'flags_x64'] = \
                        #     platform_item[SETTINGS.OPERATING_SYSTEM][u'flags_x64']
                        # plugin_dict[u'project_workspace_flag'] = \
                        #     platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_flag']
                        # plugin_dict[u'project_workspace_parent_directory_level'] = \
                        #     platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_parent_directory_level']
                        # plugin_dict[u'project_file_flag'] = \
                        #     platform_item[SETTINGS.OPERATING_SYSTEM][u'project_file_flag']
                        if executable in executable_list:
                            plugin_dict[u'executable'] = executable
                        else:
                            plugin_dict[u'executable'] = None
                        # if executable_x64 in executable_list:
                        #     plugin_dict[u'executable_x64'] = executable_x64
                        # else:
                        #     plugin_dict[u'executable_x64'] = None

                        plugin_list.append(plugin_dict.copy())

            elif plugin_object[u'type'] == 'plugin':
                pass

            elif plugin_object[u'type'] == 'standalone':

                architecture_fallback = None

                # print release

                if release[u'architecture_agnostic']:
                    # if SETTINGS.ARCHITECTURE == 'x64' and release[u'architecture_fallback']:
                    #     architecture_fallback = True
                    # elif SETTINGS.ARCHITECTURE == 'x32':
                    #     architecture_fallback = False

                    label = str(plugin_object[u'vendor'] + ' ' +
                                plugin_object[u'family'] + ' ' +
                                release[u'release_number'])
                    # label_x64 = str(plugin_object[u'vendor'] + ' ' +
                    #                 plugin_object[u'family'] + ' ' +
                    #                 release[u'release_number'] +
                    #                 ' (%s)' % SETTINGS.ARCHITECTURES[SETTINGS.ARCHITECTURES.index('x64')])

                    project_directories_list = []

                    for project_directory in release[u'project_directories']:
                        project_directory = project_directory.replace('%', os.sep)
                        project_directories_list.append(project_directory)

                    for platform_item in release[u'platforms']:
                        if SETTINGS.OPERATING_SYSTEM in platform_item:
                            executable = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable']
                            # executable_x64 = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable_x64']

                            executable_list = []

                            # for executable in [executable_x32, executable_x64]:
                            if executable is None:
                                logging.warning('executable is %s' % executable)
                            elif os.path.exists(executable):
                                executable_list.append(executable)
                                logging.info('executable %s found on this machine.' % executable)
                            elif not os.path.exists(executable):
                                logging.warning('executable %s not found on this machine.' % executable)

                            plugin_dict[u'family'] = \
                                plugin_object[u'family']
                            plugin_dict[u'type'] = \
                                plugin_object[u'type']
                            plugin_dict[u'nodeable'] = \
                                plugin_object[u'nodeable']
                            # plugin_dict[u'node_only'] = \
                            #     plugin_object[u'node_only']
                            plugin_dict[u'family_enable'] = \
                                plugin_object[u'family_enable']
                            plugin_dict[u'vendor'] = \
                                plugin_object[u'vendor']
                            plugin_dict[u'abbreviation'] = \
                                plugin_object[u'abbreviation']
                            plugin_dict[u'release_number'] = \
                                release[u'release_number']
                            if release[u'icon'] is None:
                                plugin_dict[u'icon'] = release[u'icon']
                            else:
                                plugin_dict[u'icon'] = \
                                    os.path.join(SETTINGS.PLUGINS_ICONS, release[u'icon'])
                            plugin_dict[u'release_extension'] = \
                                release[u'release_extension']
                            plugin_dict[u'project_template'] = \
                                release[u'project_template']
                            plugin_dict[u'project_workspace_template'] = \
                                release[u'project_workspace_template']
                            plugin_dict[u'default_outputs'] = \
                                release[u'default_outputs']
                            plugin_dict[u'architecture_agnostic'] = \
                                release[u'architecture_agnostic']
                            plugin_dict[u'architecture_fallback'] = \
                                architecture_fallback
                            plugin_dict[u'label'] = \
                                label_x32
                            plugin_dict[u'label'] = \
                                label_x64
                            plugin_dict[u'project_directories'] = \
                                project_directories_list
                            plugin_dict[u'flags'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'flags']
                            # plugin_dict[u'flags_x64'] = \
                            #     platform_item[SETTINGS.OPERATING_SYSTEM][u'flags_x64']
                            plugin_dict[u'project_workspace_flag'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_flag']
                            plugin_dict[u'project_workspace_parent_directory_level'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_parent_directory_level']
                            plugin_dict[u'project_file_flag'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_file_flag']
                            # if executable_x32 in executable_list:
                            plugin_dict[u'executable'] = executable
                            # else:
                            #     plugin_dict[u'executable_x32'] = None
                            # if executable_x64 in executable_list:
                            #     plugin_dict[u'executable_x64'] = executable_x64
                            # else:
                            #     plugin_dict[u'executable_x64'] = None

                            plugin_list.append(plugin_dict.copy())

                else:
                    if SETTINGS.ARCHITECTURE == 'x64' and release[u'architecture_fallback']:
                        architecture_fallback = True
                    elif SETTINGS.ARCHITECTURE == 'x32':
                        architecture_fallback = False

                    label_x32 = str(plugin_object[u'vendor'] + ' ' +
                                    plugin_object[u'family'] + ' ' +
                                    release[u'release_number'] +
                                    ' (%s)' % SETTINGS.ARCHITECTURES[SETTINGS.ARCHITECTURES.index('x32')])
                    label_x64 = str(plugin_object[u'vendor'] + ' ' +
                                    plugin_object[u'family'] + ' ' +
                                    release[u'release_number'] +
                                    ' (%s)' % SETTINGS.ARCHITECTURES[SETTINGS.ARCHITECTURES.index('x64')])

                    project_directories_list = []

                    for project_directory in release[u'project_directories']:
                        project_directory = project_directory.replace('%', os.sep)
                        project_directories_list.append(project_directory)

                    for platform_item in release[u'platforms']:
                        if SETTINGS.OPERATING_SYSTEM in platform_item:
                            executable_x32 = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable_x32']
                            executable_x64 = platform_item[SETTINGS.OPERATING_SYSTEM][u'executable_x64']

                            executable_list = []

                            for executable in [executable_x32, executable_x64]:
                                if executable is None:
                                    logging.warning('executable is %s' % executable)
                                elif os.path.exists(executable):
                                    executable_list.append(executable)
                                    logging.info('executable %s found on this machine.' % executable)
                                elif not os.path.exists(executable):
                                    logging.warning('executable %s not found on this machine.' % executable)

                            plugin_dict[u'family'] = \
                                plugin_object[u'family']
                            plugin_dict[u'type'] = \
                                plugin_object[u'type']
                            plugin_dict[u'nodeable'] = \
                                plugin_object[u'nodeable']
                            # plugin_dict[u'node_only'] = \
                            #     plugin_object[u'node_only']
                            plugin_dict[u'family_enable'] = \
                                plugin_object[u'family_enable']
                            plugin_dict[u'vendor'] = \
                                plugin_object[u'vendor']
                            plugin_dict[u'abbreviation'] = \
                                plugin_object[u'abbreviation']
                            plugin_dict[u'release_number'] = \
                                release[u'release_number']
                            if release[u'icon'] is None:
                                plugin_dict[u'icon'] = release[u'icon']
                            else:
                                plugin_dict[u'icon'] = \
                                    os.path.join(SETTINGS.PLUGINS_ICONS, release[u'icon'])
                            plugin_dict[u'release_extension'] = \
                                release[u'release_extension']
                            plugin_dict[u'project_template'] = \
                                release[u'project_template']
                            plugin_dict[u'project_workspace_template'] = \
                                release[u'project_workspace_template']
                            plugin_dict[u'default_outputs'] = \
                                release[u'default_outputs']
                            plugin_dict[u'architecture_agnostic'] = \
                                release[u'architecture_agnostic']
                            plugin_dict[u'architecture_fallback'] = \
                                architecture_fallback
                            plugin_dict[u'label_x32'] = \
                                label_x32
                            plugin_dict[u'label_x64'] = \
                                label_x64
                            plugin_dict[u'project_directories'] = \
                                project_directories_list
                            plugin_dict[u'flags_x32'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'flags_x32']
                            plugin_dict[u'flags_x64'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'flags_x64']
                            plugin_dict[u'project_workspace_flag'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_flag']
                            plugin_dict[u'project_workspace_parent_directory_level'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_workspace_parent_directory_level']
                            plugin_dict[u'project_file_flag'] = \
                                platform_item[SETTINGS.OPERATING_SYSTEM][u'project_file_flag']
                            if executable_x32 in executable_list:
                                plugin_dict[u'executable_x32'] = executable_x32
                            else:
                                plugin_dict[u'executable_x32'] = None
                            if executable_x64 in executable_list:
                                plugin_dict[u'executable_x64'] = executable_x64
                            else:
                                plugin_dict[u'executable_x64'] = None

                            plugin_list.append(plugin_dict.copy())

    return plugin_list


def get_plugins():
    plugin_objects = []
    plugins = parse_plugins()
    for plugin in plugins:
        new_plugin_object = class_plugin.PlugIn(plugin)
        plugin_objects.append(new_plugin_object)

    return plugin_objects

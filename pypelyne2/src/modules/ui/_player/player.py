import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import PyQt4.uic as uic
import logging
import threading
import os
import random
import src.conf.settings.SETTINGS as SETTINGS
import src.modules.vlc.vlc as vlc


class Player(QtGui.QWidget):
    def __init__(self):
        super(Player, self).__init__()

        self.ui = uic.loadUi(os.path.join(SETTINGS.PYPELYNE2_ROOT, 'src', 'modules', 'ui', 'player', 'player.ui'), self)

        self.player_context_menu = QtGui.QMenu()
        self.menu_album = None
        self.player_exists = False
        self.audio_folder_content = []

        self.mlp = vlc.MediaListPlayer()
        self.mp = vlc.MediaPlayer()
        self.mlp.set_media_player(self.mp)

        self.ml = vlc.MediaList()

    def add_player(self):
        # self.horizontalLayout.addWidget(self.ui)
        self.ui.push_button_play_stop.clicked.connect(self.play_audio)

        self.ui.push_button_play_stop.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.connect(self.ui.push_button_play_stop,
                     QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'),
                     self.player_context_menu_show)

        q_menu_titles = []

        for dirs, subdirs, files in os.walk(SETTINGS.MP3_ROOT, topdown=False):
            for single_file in files:
                if single_file in SETTINGS.EXCLUSIONS:
                    os.remove(os.path.join(dirs, single_file))
                    logging.warning('file %s deleted from %s' % (single_file, dirs))

                elif os.path.splitext(single_file)[1] not in SETTINGS.AUDIO_EXTENSIONS:
                    logging.warning('non audio file %s found in %s' % (single_file, dirs))

                else:
                    if not os.path.relpath(dirs, SETTINGS.MP3_ROOT) == '.':
                        q_menu_name = os.path.relpath(dirs, SETTINGS.MP3_ROOT)
                        # if len(q_menu_name.split(os.sep)) > 1:
                        if q_menu_name not in q_menu_titles:
                            self.menu_album = self.player_context_menu.addMenu(q_menu_name.replace(os.sep, ' - '))
                            q_menu_titles.append(q_menu_name)

                            self.menu_album.addAction(single_file,
                                                      self.play_audio_callback(os.path.join(dirs, single_file)))
                            self.audio_folder_content.append(os.path.join(dirs, single_file))
                        else:
                            self.menu_album.addAction(single_file,
                                                      self.play_audio_callback(os.path.join(dirs, single_file)))
                            self.audio_folder_content.append(os.path.join(dirs, single_file))

                    else:
                        self.player_context_menu.addAction(single_file,
                                                           self.play_audio_callback(os.path.join(dirs, single_file)))
                        self.audio_folder_content.append(os.path.join(dirs, single_file))

        self.ui.push_button_play_stop.setText('play')
        # self.player_exists = False

    def player_context_menu_show(self, point):
        self.player_context_menu.exec_(self.ui.push_button_play_stop.mapToGlobal(point))

    def play_audio_callback(self, track=None):
        def callback():
            self.play_audio(track)
        return callback

    # def player_context_menu(self, point):
    #     self.player_context_menu.exec_(self.ui.push_button_play_stop.mapToGlobal(point))

    def play_audio(self, track=None):
        track_id = None

        # https://forum.videolan.org/viewtopic.php?t=107039
        if len(os.listdir(SETTINGS.MP3_ROOT)) == 0:
            logging.warning('no audio files found')
            self.ui.radioButtonPlay.setEnabled(False)

        elif not self.player_exists:
            random.shuffle(self.audio_folder_content, random.random)

            if not track:
                track_id = self.audio_folder_content.index(track)

            for audio_file in self.audio_folder_content:
                self.ml.add_media(os.path.join(SETTINGS.MP3_ROOT, audio_file))

            self.mlp.set_media_list(self.ml)

            if track:
                self.mlp.play_item_at_index(track_id)
                logging.info('playing {0}'.format(track_id))

            else:
                self.mlp.play()
                logging.info('playing randomly')

            self.player_exists = True

            self.ui.push_button_play_stop.clicked.disconnect(self.play_audio)
            self.ui.push_button_play_stop.clicked.connect(self.stopAudio)
            self.ui.push_button_play_stop.setText('stop')
            logging.info('setting push_button_play_stop function to stop')
            threading.Timer(0.5, self.from_stop_to_skip).start()

        elif self.player_exists and track:
            logging.info('playing {0}'.format(track))
            track_id = self.audio_folder_content.index(track)
            self.skip_audio(track_id)

        else:
            logging.info('already on air')

    def from_stop_to_skip(self):
        if self.player_exists:
            self.ui.push_button_play_stop.clicked.disconnect(self.stopAudio)
            self.ui.push_button_play_stop.clicked.connect(self.skip_audio)
            self.ui.push_button_play_stop.setText('skip')
            logging.info('setting push_button_play_stop function to skip')

    def from_skip_to_stop(self):
        if self.player_exists:
            self.ui.push_button_play_stop.clicked.disconnect(self.skip_audio)
            self.ui.push_button_play_stop.clicked.connect(self.stopAudio)
            self.ui.push_button_play_stop.setText('stop')
            logging.info('setting push_button_play_stop function to stop')

    def stop_audio(self):
        if self.player_exists:
            try:
                self.ui.push_button_play_stop.clicked.disconnect(self.stopAudio)
                self.ui.push_button_play_stop.clicked.connect(self.play_audio)
                self.mp.stop()
                self.mp.release()
                self.mlp.release()
                self.player_exists = False
                self.ui.push_button_play_stop.setText('play')
                logging.info('setting push_button_play_stop function to play')
            except Exception, e:
                logging.warning('error or not playing {0}'.format(e))

    def skip_audio(self, track_id=None):
        if self.player_exists:
            if track_id:
                self.mlp.play_item_at_index(track_id)

            else:
                self.mlp.next()

            self.ui.push_button_play_stop.clicked.disconnect(self.skip_audio)
            self.ui.push_button_play_stop.clicked.connect(self.stopAudio)
            self.ui.push_button_play_stop.setText('stop')
            threading.Timer(0.5, self.from_stop_to_skip).start()

import os
from PyQt4 import QtGui
from PyQt4 import uic
# from PyQt4.QtGui import *
# from PyQt4.uic import *
from vlc import *


class PlayerUi(QWidget):
    def __init__(self, parent = None):
        super(PlayerUi, self).__init__(parent)
        self.pypelyne_root = os.getcwd()

        self.ui = uic.loadUi(os.path.join(os.path.dirname(self.main_window.pypelyne_root), 'ui', 'player.ui'), self)
        #self.ui = loadUi(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\ui\player.ui')

        self.player = None

        #self.create_connects()


    def createConnects(self):
        self.radioButtonPlay.toggled.connect(self.play)
        self.radioButtonStop.toggled.connect(self.stop)

    def play(self):
        self.player = MediaPlayer(r'C:\Users\michael.mussato.SCHERRERMEDIEN\Dropbox\development\workspace\PyPELyNE\src\audio\cairnomount.mp3')
        self.player.play()

    def stop(self):
        try:
            self.player.stop()
        except:
            pass


if __name__ == "__main__":

    app = QApplication(sys.argv)
    playerWindow = playerUi()
    #screen_size = QApplication.desktop().availableGeometry()

    playerUi.show()
    app.exec_()



    
    # def add_player(self):
    #     self.player_ui = PlayerWidgetUi(self)
    #     self.horizontalLayout.addWidget(self.player_ui)
    #     # self.player_ui.radioButtonPlay.clicked.connect(self.play_audio)
    #     self.player_ui.pushButtonPlayStop.clicked.connect(self.play_audio)
    #
    #     self.player_ui.pushButtonPlayStop.setContextMenuPolicy(Qt.CustomContextMenu)
    #     self.connect(self.player_ui.pushButtonPlayStop, SIGNAL('customContextMenuRequested(const QPoint&)'), self.player_context_menu)
    #
    #     self.player_context_menu = QMenu()
    #     q_menu_titles = []
    #
    #     for dir, subdirs, files in os.walk(SETTINGS.AUDIO_FOLDER_DARWIN, topdown=False):
    #         for file in files:
    #             if file in SETTINGS.EXCLUSIONS:
    #                 os.remove(os.path.join(dir, file))
    #                 logging.warning('file %s deleted from %s' % (file, dir))
    #
    #             elif os.path.splitext(file)[1] not in SETTINGS.AUDIO_EXTENSIONS:
    #                 logging.warning('non audio file %s found in %s' % (file, dir))
    #
    #             else:
    #                 if not os.path.relpath(dir, SETTINGS.AUDIO_FOLDER_DARWIN) == '.':
    #                     q_menu_name = os.path.relpath(dir, SETTINGS.AUDIO_FOLDER_DARWIN)
    #                     # if len(q_menu_name.split(os.sep)) > 1:
    #                     if q_menu_name not in q_menu_titles:
    #                         self.menuAlbum = self.player_context_menu.addMenu(q_menu_name.replace(os.sep, ' - '))
    #                         q_menu_titles.append(q_menu_name)
    #
    #                         self.menuAlbum.addAction(file, self.play_audio_callback(os.path.join(dir, file)))
    #                         self.audio_folder_content.append(os.path.join(dir, file))
    #                     else:
    #                         self.menuAlbum.addAction(file, self.play_audio_callback(os.path.join(dir, file)))
    #                         self.audio_folder_content.append(os.path.join(dir, file))
    #
    #                 else:
    #                     self.player_context_menu.addAction(file, self.play_audio_callback(os.path.join(dir, file)))
    #                     self.audio_folder_content.append(os.path.join(dir, file))
    #
    #     self.player_ui.pushButtonPlayStop.setText('play')
    #     self.player_exists = False
    #
    # def player_context_menu(self, point):
    #     self.player_context_menu.exec_(self.player_ui.pushButtonPlayStop.mapToGlobal(point))
    #
    # def play_audio_callback(self, track=None):
    #     def callback():
    #         self.play_audio(track)
    #     return callback
    #
    # def play_audio(self, track=None):
    #     # https://forum.videolan.org/viewtopic.php?t=107039
    #     if len(os.listdir(SETTINGS.AUDIO_FOLDER_DARWIN)) == 0:
    #         logging.warning('no audio files found')
    #         self.player_ui.radioButtonPlay.setEnabled(False)
    #
    #     elif not self.player_exists:
    #         random.shuffle(self.audio_folder_content, random.random)
    #
    #         if not track:
    #             track_id = self.audio_folder_content.index(track)
    #
    #         self.mlp = MediaListPlayer()
    #         self.mp = MediaPlayer()
    #         self.mlp.set_media_player(self.mp)
    #
    #         self.ml = MediaList()
    #
    #         for file in self.audio_folder_content:
    #             self.ml.add_media(os.path.join(SETTINGS.AUDIO_FOLDER_DARWIN, file))
    #
    #         self.mlp.set_media_list(self.ml)
    #
    #         if track:
    #             self.mlp.play_item_at_index(track_id)
    #             logging.info('playing %s' % track_id)
    #
    #         else:
    #             self.mlp.play()
    #             logging.info('playing randomly')
    #
    #         self.player_exists = True
    #
    #         self.player_ui.pushButtonPlayStop.clicked.disconnect(self.play_audio)
    #         self.player_ui.pushButtonPlayStop.clicked.connect(self.stopAudio)
    #         self.player_ui.pushButtonPlayStop.setText('stop')
    #         logging.info('setting pushButtonPlayStop function to stop')
    #         threading.Timer(0.5, self.from_stop_to_skip).start()
    #
    #     elif self.player_exists and track:
    #         logging.info('playing %s' % track)
    #         track_id = self.audio_folder_content.index(track)
    #         self.skip_audio(track_id)
    #
    #     else:
    #         logging.info('already on air')
    #
    # def from_stop_to_skip(self):
    #     if self.player_exists:
    #         self.player_ui.pushButtonPlayStop.clicked.disconnect(self.stopAudio)
    #         self.player_ui.pushButtonPlayStop.clicked.connect(self.skip_audio)
    #         self.player_ui.pushButtonPlayStop.setText('skip')
    #         logging.info('setting pushButtonPlayStop function to skip')
    #
    # def from_skip_to_stop(self):
    #     if self.player_exists:
    #         self.player_ui.pushButtonPlayStop.clicked.disconnect(self.skip_audio)
    #         self.player_ui.pushButtonPlayStop.clicked.connect(self.stopAudio)
    #         self.player_ui.pushButtonPlayStop.setText('stop')
    #         logging.info('setting pushButtonPlayStop function to stop')
    #
    # def stop_audio(self):
    #     if self.player_exists:
    #         try:
    #             self.player_ui.pushButtonPlayStop.clicked.disconnect(self.stopAudio)
    #             self.player_ui.pushButtonPlayStop.clicked.connect(self.play_audio)
    #             self.mp.stop()
    #             self.mp.release()
    #             self.mlp.release()
    #             self.player_exists = False
    #             self.player_ui.pushButtonPlayStop.setText('play')
    #             logging.info('setting pushButtonPlayStop function to play')
    #             #logging.info('audio stopped')
    #         except:
    #             logging.warning('error or not playing')
    #
    # def skip_audio(self, track_id=None):
    #     if self.player_exists:
    #         if track_id:
    #             self.mlp.play_item_at_index(track_id)
    #
    #         else:
    #             self.mlp.next()
    #
    #         self.player_ui.pushButtonPlayStop.clicked.disconnect(self.skip_audio)
    #         self.player_ui.pushButtonPlayStop.clicked.connect(self.stopAudio)
    #         self.player_ui.pushButtonPlayStop.setText('stop')
    #         threading.Timer(0.5, self.from_stop_to_skip).start()
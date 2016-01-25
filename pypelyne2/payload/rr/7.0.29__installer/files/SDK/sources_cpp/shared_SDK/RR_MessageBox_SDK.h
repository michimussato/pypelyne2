#ifndef RR_MessageBox_H
#define RR_MessageBox_H

#ifdef QT_CORE_LIB

#ifdef rrConsoleApp
#include <stdio.h>
#include <QString>


class rrMessageBox
{
public:
    static bool NoIcon(void * ,const QString &message) {printf("%s",message.toLatin1().data()); return true;}
    static bool Question(void * ,const QString &message,const QString &,const int ,const QString &, bool * ) {printf("%s",message.toLatin1().data()); return true;}
    static bool Information(void * ,const QString &message) {printf("%s",message.toLatin1().data()); return true;}
    static bool Warning(void * ,const QString &message) {printf("%s",message.toLatin1().data()); return true;}
    static bool Critical(void * ,const QString &message) {printf("%s",message.toLatin1().data()); return true;}
};



#else // not rrConsoleApp

#include <QMessageBox>
class QPushButton;
class QAction;
class QSpacerItem;


class rrMessageBox: public QDialog
{
	   Q_OBJECT
public:
	rrMessageBox(QWidget * parent, const QMessageBox::Icon iconType, const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed=NULL,const bool &modal=true,bool centerText=true,bool courier=false);
	static QPixmap standardIcon(QMessageBox::Icon icon);
    QPushButton * Btn;
    QPushButton * Btn2;
	QPushButton * CancelButton;
	QSpacerItem *btnL,*btnR;
	QString btnText;
    QLabel * iconLabel;
	QLabel * blabla;
	QLabel * blablaCTRLC;
	QAction  * ActionClipBoard;
	QAction  * ActionHotKey1;
	QAction  * ActionHotKey2;
    QString currentMessage;
	bool * CancelResult;
	static bool NoIcon(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=30,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Question(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=30,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Information(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=30,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Information_noCenter(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=30,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Information_noCenterCourier(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=30,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Warning(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=45,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);
	static bool Critical(QWidget * parent,const QString &message,const QString &buttontext="Ok",const int waittime=90,const QString &buttontext2="", bool * cancelPressed=NULL,bool courier=false);

private slots:
	void copyToClipBoard();
	void Button1Pressed();
	void Button2Pressed();

private:
	int seconds;

protected:
	void timerEvent(QTimerEvent *event);	
};

class rrMessageBox4Buttons: public QDialog
{
	   Q_OBJECT
public:
	rrMessageBox4Buttons(QWidget * parent, const QMessageBox::Icon iconType, const QString &message,const QString &buttontext1,const QString &buttontext2,const QString &buttontext3=QString(),const QString &buttontext4=QString());
    QPushButton * Btn1;
    QPushButton * Btn2;
    QPushButton * Btn3;
    QPushButton * Btn4;
	QPushButton * CancelButton;
	QSpacerItem *btnL,*btnR;
    QLabel * iconLabel;
	QLabel * blabla;
	QLabel * blablaCTRLC;
	QAction  * ActionClipBoard;
	QAction  * ActionHotKey1;
	QAction  * ActionHotKey2;
	QAction  * ActionHotKey3;
	QAction  * ActionHotKey4;
    QString currentMessage;
	bool * CancelResult;
	int  resultID;
	static int Question(QWidget * parent, const QString &message,const QString &buttontext1,const QString &buttontext2,const QString &buttontext3=QString(),const QString &buttontext4=QString());

private slots:
	void copyToClipBoard();
	void Button1Pressed();
	void Button2Pressed();
	void Button3Pressed();
	void Button4Pressed();

};
#endif //not rrConsoleApp

#endif //qt_core

#endif


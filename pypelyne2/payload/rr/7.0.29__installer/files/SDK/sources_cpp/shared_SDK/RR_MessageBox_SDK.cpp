

#include "RR_MessageBox_SDK.h"

#ifndef rrConsoleApp
#include <QGridLayout>
#include <QLabel>
#include <QApplication>
#include <QClipboard>
#include <QStyle>
#include <QPushButton>
#include <QAction>
#include <QStringList>
#include <QThread>
#include "RR_defines_SDK.h"
#if (defined(RR_OS_WIN) && defined(defbaTimeSheet))
	#include "Windows.h"
#endif


QPixmap rrMessageBox::standardIcon(QMessageBox::Icon icon)
{
    QStyle *style = QApplication::style();
    int iconSize = style->pixelMetric(QStyle::PM_MessageBoxIconSize, 0, 0);
    QIcon tmpIcon;
    switch (icon) {
    case QMessageBox::Information:
        tmpIcon = style->standardIcon(QStyle::SP_MessageBoxInformation, 0, 0);
        break;
    case QMessageBox::Warning:
        tmpIcon = style->standardIcon(QStyle::SP_MessageBoxWarning, 0, 0);
        break;
    case QMessageBox::Critical:
        tmpIcon = style->standardIcon(QStyle::SP_MessageBoxCritical, 0, 0);
        break;
    case QMessageBox::Question:
        tmpIcon = style->standardIcon(QStyle::SP_MessageBoxQuestion, 0, 0);
    default:
        break;
    }
    if (!tmpIcon.isNull())
        return tmpIcon.pixmap(iconSize, iconSize);
    return QPixmap();
}



rrMessageBox::rrMessageBox(QWidget * parent,const QMessageBox::Icon iconType, const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed,const bool &modal,bool centerText,bool courier)
	: QDialog(parent)
{
    this->setMaximumSize(QSize(1200, 1000));
	QString Hotkey1;
	QString Hotkey2;

	if (!buttontext.isEmpty())  {
		if (buttontext.startsWith('&')) 
			Hotkey1=buttontext.at(1).toLower();
		else
			Hotkey1=buttontext.at(0).toLower();
	}
	if (!buttontext2.isEmpty()) {
		if (buttontext2.startsWith('&')) 
			Hotkey2=buttontext2.at(1).toLower();
		else
			Hotkey2=buttontext2.at(0).toLower();
	}

	if (Hotkey1==Hotkey2) {
		Hotkey1.clear();
		Hotkey2.clear();
	}

	CancelResult=cancelPressed;
	QHBoxLayout * HLay = new QHBoxLayout(this);

	if ((iconType!=QMessageBox::Information) && (iconType!=QMessageBox::Question) ) {
		iconLabel = new QLabel(this);
		iconLabel->setPixmap(standardIcon(iconType));
		HLay->addWidget(iconLabel,0,Qt::AlignTop);
	}

	QVBoxLayout * VLay = new QVBoxLayout();
	VLay->setSpacing(7);
	VLay->setContentsMargins(0,0,0,0);


	blabla  = new QLabel(this);
	blabla->setText(message+"\n");
	if (centerText)	blabla->setAlignment(Qt::AlignCenter);
	if (courier) blabla->setFont(QFont("Courier"));
    VLay->addWidget(blabla, Qt::AlignCenter);

    QHBoxLayout * btnLayout = new QHBoxLayout();
	btnLayout->setSpacing(20);
	btnLayout->setContentsMargins(0,0,0,0);

	btnL = new QSpacerItem (5,5,QSizePolicy::Expanding,QSizePolicy::Minimum);
	btnR = new QSpacerItem (5,5,QSizePolicy::Expanding,QSizePolicy::Minimum);
	btnLayout->addItem(btnL);

    Btn = new QPushButton(this);
	Btn->setText(buttontext);
	btnText=buttontext;
    connect(Btn, SIGNAL(clicked()), this, SLOT(Button1Pressed()));
    Btn->setFocus();
	Btn->setMinimumSize(QSize(130, 20));
    btnLayout->addWidget(Btn,  0,  Qt::AlignCenter);

	if (!buttontext2.isEmpty()) {
		Btn2 = new QPushButton(this);
		Btn2->setText(buttontext2);
		Btn2->setMinimumSize(QSize(130, 20));
		connect(Btn2, SIGNAL(clicked()), this, SLOT(Button2Pressed()));
		btnLayout->addWidget(Btn2, 0, Qt::AlignCenter);
	}
	btnLayout->addItem(btnR);

	VLay->addLayout(btnLayout);

	if (CancelResult!=NULL) {
		*CancelResult=true; //set cancel in case dialog is closed, NO cancel only if button 2 is pressed
		CancelButton = new QPushButton(this);
		CancelButton->setText("cancel");
		CancelButton->setMaximumSize(QSize(50, 16));
		connect(CancelButton, SIGNAL(clicked()), this, SLOT(reject()));
		VLay->addWidget(CancelButton, 0,  Qt::AlignCenter);
	}

	blablaCTRLC  = new QLabel(this);
#ifdef RR_OS_WIN
	blablaCTRLC->setText("<font color=\"#999999\">Copy message text with CTRL-C (Paste in any editor before app closes)</font>");
#else
	blablaCTRLC->setText("<font color=\"#999999\">Copy message text with CTRL-C</font>");
#endif
	blablaCTRLC->setFont(QFont("Arial",7));
	blablaCTRLC->setAlignment(Qt::AlignCenter);
    VLay->addWidget(blablaCTRLC  ,  Qt::AlignCenter);


	HLay->addLayout(VLay);
	HLay->setSpacing(10);
	HLay->setContentsMargins(10,20,25,0);

	seconds=waittime;
	if (waittime>0) {
		startTimer(1000);
		Btn->setText(btnText + QString("  (%1)").arg(seconds));
	}
	
	ActionHotKey1=NULL;
	ActionHotKey2=NULL;
	
	if (!Hotkey1.isEmpty()) {
		ActionHotKey1 = new QAction(this);
		ActionHotKey1->setShortcut(Hotkey1);
		connect(ActionHotKey1, SIGNAL(triggered()), this, SLOT(Button1Pressed()));
		addAction(ActionHotKey1);
	}
	if (!Hotkey2.isEmpty()) {
		ActionHotKey2 = new QAction(this);
		ActionHotKey2->setShortcut(Hotkey2);
		connect(ActionHotKey2, SIGNAL(triggered()), this, SLOT(Button2Pressed()));
		addAction(ActionHotKey2);
	}


    ActionClipBoard = new QAction(this);
    ActionClipBoard->setShortcut(tr("Ctrl+C"));
	connect(ActionClipBoard, SIGNAL(triggered()), this, SLOT(copyToClipBoard()));
	addAction(ActionClipBoard);
	setModal(modal);
	if (modal) exec();
}


void rrMessageBox::timerEvent(QTimerEvent * /*event*/) {
	seconds--;
	Btn->setText(btnText + QString("  (%1)").arg(seconds));
	if (seconds<=0) accept();	
}

void rrMessageBox::copyToClipBoard()
{
	QClipboard *clipboard = QApplication::clipboard();
	clipboard->setText(blabla->text());
}


void rrMessageBox::Button2Pressed()
{
	if (CancelResult!=NULL) {
		*CancelResult=false;
	}
	reject();
}

void rrMessageBox::Button1Pressed()
{
	if (CancelResult!=NULL) {
		*CancelResult=false;
	}
	accept();
}



bool rrMessageBox::NoIcon(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::NoIcon,message,buttontext,waittime,buttontext2,cancelPressed,true,!courier,courier);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Question(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Question,message,buttontext,waittime,buttontext2,cancelPressed,true,!courier,courier);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Warning(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Warning,message,buttontext,waittime,buttontext2,cancelPressed,true,!courier,courier);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Information(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Information,message,buttontext,waittime,buttontext2,cancelPressed,true,!courier,courier);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Information_noCenter(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Information,message,buttontext,waittime,buttontext2,cancelPressed,true,false,courier);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Information_noCenterCourier(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool )
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Information,message,buttontext,waittime,buttontext2,cancelPressed,true,false,true);
	return (ShowIt.result()==QDialog::Accepted);
}

bool rrMessageBox::Critical(QWidget * parent,const QString &message,const QString &buttontext,const int waittime,const QString &buttontext2, bool * cancelPressed, bool courier)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox ShowIt(parent,QMessageBox::Critical,message,buttontext,waittime,buttontext2,cancelPressed,true,!courier,courier);
	return (ShowIt.result()==QDialog::Accepted);
}







rrMessageBox4Buttons::rrMessageBox4Buttons(QWidget * parent, const QMessageBox::Icon iconType, const QString &message,const QString &buttontext1,const QString &buttontext2,const QString &buttontext3,const QString &buttontext4)
	: QDialog(parent)
{
	QString Hotkey1;
	QString Hotkey2;
	QString Hotkey3;
	QString Hotkey4;

	if (!buttontext1.isEmpty())
		Hotkey1=buttontext1.at(0).toLower();
	if (!buttontext2.isEmpty())
		Hotkey2=buttontext2.at(0).toLower();
	if (!buttontext3.isEmpty())
		Hotkey3=buttontext3.at(0).toLower();
	if (!buttontext4.isEmpty())
		Hotkey4=buttontext4.at(0).toLower();

	QHBoxLayout * HLay = new QHBoxLayout(this);

	if ((iconType!=QMessageBox::Information) && (iconType!=QMessageBox::Question) ) {
		iconLabel = new QLabel(this);
		iconLabel->setPixmap(rrMessageBox::standardIcon(iconType));
		HLay->addWidget(iconLabel,0,Qt::AlignTop);
	}

	QVBoxLayout * VLay = new QVBoxLayout();
	VLay->setSpacing(7);
	VLay->setContentsMargins(0,0,0,0);

	blabla  = new QLabel(this);
	blabla->setText(message+"\n");
//	if (centerText)	blabla->setAlignment(Qt::AlignCenter);
//	if (courier) blabla->setFont(QFont("Courier"));
    VLay->addWidget(blabla, Qt::AlignCenter);

    QHBoxLayout * btnLayout = new QHBoxLayout();
	btnLayout->setSpacing(20);
	btnLayout->setContentsMargins(0,0,0,0);

	btnL = new QSpacerItem (5,5,QSizePolicy::Expanding,QSizePolicy::Minimum);
	btnR = new QSpacerItem (5,5,QSizePolicy::Expanding,QSizePolicy::Minimum);
	btnLayout->addItem(btnL);

	if (!buttontext1.isEmpty()) {
	    Btn1 = new QPushButton(this);
		Btn1->setText(buttontext1);
	    connect(Btn1, SIGNAL(clicked()), this, SLOT(Button1Pressed()));
		if (buttontext1.contains('\n'))
			Btn1->setMinimumSize(QSize(130, 35));
		else
			Btn1->setMinimumSize(QSize(130, 20));
	    btnLayout->addWidget(Btn1,  0,  Qt::AlignCenter);
		Btn1->setFocus();  //Unique to button 1
	}


	if (!buttontext2.isEmpty()) {
		Btn2 = new QPushButton(this);
		Btn2->setText(buttontext2);
		if (buttontext2.contains('\n'))
			Btn2->setMinimumSize(QSize(130, 35));
		else
			Btn2->setMinimumSize(QSize(130, 20));
		connect(Btn2, SIGNAL(clicked()), this, SLOT(Button2Pressed()));
		btnLayout->addWidget(Btn2, 0, Qt::AlignCenter);
	}
	if (!buttontext3.isEmpty()) {
		Btn3 = new QPushButton(this);
		Btn3->setText(buttontext3);
		if (buttontext3.contains('\n'))
			Btn3->setMinimumSize(QSize(130, 35));
		else
			Btn3->setMinimumSize(QSize(130, 20));
		connect(Btn3, SIGNAL(clicked()), this, SLOT(Button3Pressed()));
		btnLayout->addWidget(Btn3, 0, Qt::AlignCenter);
	}
	if (!buttontext4.isEmpty()) {
		Btn4 = new QPushButton(this);
		Btn4->setText(buttontext4);
		if (buttontext4.contains('\n'))
			Btn4->setMinimumSize(QSize(130, 35));
		else
			Btn4->setMinimumSize(QSize(130, 20));
		connect(Btn4, SIGNAL(clicked()), this, SLOT(Button4Pressed()));
		btnLayout->addWidget(Btn4, 0, Qt::AlignCenter);
	}
	btnLayout->addItem(btnR);

	VLay->addLayout(btnLayout);

	CancelButton = new QPushButton(this);
	CancelButton->setText("cancel");
	CancelButton->setMaximumSize(QSize(50, 16));
	connect(CancelButton, SIGNAL(clicked()), this, SLOT(reject()));
	VLay->addWidget(CancelButton, 0,  Qt::AlignCenter);

	blablaCTRLC  = new QLabel(this);
#ifdef RR_OS_WIN
	blablaCTRLC->setText("<font color=\"#999999\">Copy message text with CTRL-C (Paste in any editor before this app closes)</font>");
#else
	blablaCTRLC->setText("<font color=\"#999999\">Copy message text with CTRL-C</font>");
#endif
	blablaCTRLC->setFont(QFont("Arial",7));
	blablaCTRLC->setAlignment(Qt::AlignCenter);
    VLay->addWidget(blablaCTRLC  ,  Qt::AlignCenter);


	HLay->addLayout(VLay);
	HLay->setSpacing(10);
	HLay->setContentsMargins(10,20,25,0);

	ActionHotKey1=NULL;
	ActionHotKey2=NULL;
	ActionHotKey3=NULL;
	ActionHotKey4=NULL;
	
	if (!Hotkey1.isEmpty()) {
		ActionHotKey1 = new QAction(this);
		ActionHotKey1->setShortcut(Hotkey1);
		connect(ActionHotKey1, SIGNAL(triggered()), this, SLOT(Button1Pressed()));
		addAction(ActionHotKey1);
	}
	if (!Hotkey2.isEmpty()) {
		ActionHotKey2 = new QAction(this);
		ActionHotKey2->setShortcut(Hotkey2);
		connect(ActionHotKey2, SIGNAL(triggered()), this, SLOT(Button2Pressed()));
		addAction(ActionHotKey2);
	}
	if (!Hotkey3.isEmpty()) {
		ActionHotKey3 = new QAction(this);
		ActionHotKey3->setShortcut(Hotkey3);
		connect(ActionHotKey3, SIGNAL(triggered()), this, SLOT(Button3Pressed()));
		addAction(ActionHotKey3);
	}
	if (!Hotkey4.isEmpty()) {
		ActionHotKey4 = new QAction(this);
		ActionHotKey4->setShortcut(Hotkey4);
		connect(ActionHotKey4, SIGNAL(triggered()), this, SLOT(Button4Pressed()));
		addAction(ActionHotKey4);
	}


    ActionClipBoard = new QAction(this);
    ActionClipBoard->setShortcut(tr("Ctrl+C"));
	connect(ActionClipBoard, SIGNAL(triggered()), this, SLOT(copyToClipBoard()));
	addAction(ActionClipBoard);
	setModal(true);
}


void rrMessageBox4Buttons::copyToClipBoard()
{
	QClipboard *clipboard = QApplication::clipboard();
	clipboard->setText(blabla->text());
}

void rrMessageBox4Buttons::Button1Pressed()
{
	resultID=1;
	accept();
}

void rrMessageBox4Buttons::Button2Pressed()
{
	resultID=2;
	accept();
}

void rrMessageBox4Buttons::Button3Pressed()
{
	resultID=3;
	accept();
}

void rrMessageBox4Buttons::Button4Pressed()
{
	resultID=4;
	accept();
}



int rrMessageBox4Buttons::Question(QWidget * parent, const QString &message,const QString &buttontext1,const QString &buttontext2,const QString &buttontext3,const QString &buttontext4)
{
	if ((!QCoreApplication::instance()) || (QCoreApplication::instance()->thread()!= QThread::currentThread())) return false;
	rrMessageBox4Buttons ShowIt(parent,QMessageBox::Question,message,buttontext1,buttontext2,buttontext3,buttontext4);
	ShowIt.exec();
	return (ShowIt.resultID);
}


#endif // rrConsoleApp


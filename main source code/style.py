style = """
    QWidget{
        background: #2F2F2F;
        color: #fff;
    }

    QWidget#statusWidget QRadioButton#radioRunning::checked{
        color: yellow;
    }
    QWidget#statusWidget QRadioButton#radioStandby::checked{
        color: #00FF22;
    }
    QWidget#statusWidget QRadioButton#radioDisconnect::checked{
        color: red;
    }
    QWidget#statusWidget QRadioButton::unchecked{
        color: #656565;
    }
    QWidget#statusWidget QWidget{
        font:  10px;   
    }
    QTabWidget{
        color: #fff;
    }
    QLineEdit{
        color: #fff;
        padding: 1px;
        border: 2px solid #fff;
        border-radius: 8px;
    }
    QLabel{
        color: #fff;
    }
    QPushButton{
        color: #fff;
    }
    QPushButton:hover{
        background: #3F3F3F;
    }
    QComboBox {
        border: 1px solid gray;
        border-radius: 8px;
        padding: 1px 18px 1px 3px;
        min-width: 6em;
        color: #CFCFCF;
    }    

    QComboBox:!editable, QComboBox::drop-down:editable {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #3F3F3F, stop: 0.4 #434343,
                                    stop: 0.5 #585858, stop: 1.0 #636363);
    }

    /* QComboBox gets the "on" state when the popup is open */
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                    stop: 0 #D3D3D3, stop: 0.4 #D8D8D8,
                                    stop: 0.5 #DDDDDD, stop: 1.0 #3F3F3F);
    }

    QComboBox:on { /* shift the text when the popup opens */
        padding-top: 30px;
        padding-left: 4px;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 15px;

        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid; /* just a single line */
        border-top-right-radius: 3px; /* same radius as the QComboBox */
        border-bottom-right-radius: 3px;

    }

    QComboBox::down-arrow {
        image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
    }

    QComboBox::down-arrow:on { /* shift the arrow when popup is open */
        top: 1px;
        left: 1px;
    }

    QPlainTextEdit {
        color: #7F7F7F;
    }
"""
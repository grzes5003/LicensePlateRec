import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs 1.0
import "qml/controls"


Window {
    id: window
    width: 700
    minimumWidth: 700
    maximumWidth: 700
    height: 240
    minimumHeight: 240
    maximumHeight: 240
    visible: true
    color: "#1c1d20"
    title: qsTr("LicensePlateRec")

    Menu {
        id: mainmenu
        background: Rectangle {
            color: "#000000"
        }
    }

    Rectangle {
        id: rectangle
        height: 240
        color: "#2c313c"
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }

    Image {
        id: image
        width: 236
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: progressBar.top
        source: "no_video.png"
        anchors.bottomMargin: 10
        anchors.leftMargin: 10
        anchors.topMargin: 12
        fillMode: Image.PreserveAspectFit
        objectName: "image"
        cache: false
    }


    Text {
        id: txt_status
        x: 256
        y: 19
        color: "#ffffff"
        text: qsTr("Status: Waiting for data")
        anchors.left: image.right
        font.pixelSize: 12
        horizontalAlignment: Text.AlignLeft
        anchors.leftMargin: 10
        objectName: "txt_status"
    }

    Text {
        id: txt_name
        y: 49
        color: "#ffffff"
        text: qsTr("Name: [no video chosen]")
        anchors.left: image.right
        font.pixelSize: 12
        horizontalAlignment: Text.AlignLeft
        anchors.leftMargin: 10
        objectName: "txt_name"
    }

    Text {
        id: txt_duration
        y: 79
        color: "#ffffff"
        text: qsTr("Duration: [no video chosen]")
        anchors.left: image.right
        font.pixelSize: 12
        horizontalAlignment: Text.AlignLeft
        anchors.leftMargin: 10
        objectName: "txt_duration"
    }

    Text {
        id: txt_source
        y: 109
        color: "#ffffff"
        text: qsTr("Source: [no video chosen]")
        anchors.left: image.right
        font.pixelSize: 12
        horizontalAlignment: Text.AlignLeft
        anchors.leftMargin: 10
    }


    Text {
        id: txt_destination
        y: 140
        width: 64
        height: 13
        color: "#ffffff"
        text: qsTr("Destination: [program path folder]")
        anchors.left: image.right
        font.pixelSize: 12
        horizontalAlignment: Text.AlignLeft
        anchors.leftMargin: 10
    }

    SmallBtn {
        id: btn_choose_vid
        x: 494
        width: 140
        height: 30
        text: qsTr("Choose video")
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.rightMargin: 10
        onClicked: {
            fileDialog.open()
        }
    }

    SmallBtn {
        id: btn_choose_dest
        x: 494
        width: 140
        height: 30
        text: qsTr("Choose destination")
        anchors.right: parent.right
        anchors.top: parent.top
        btnIconSource: "images/svg_images/cil-folder-open.png"
        anchors.topMargin: 51
        anchors.rightMargin: 10
        onClicked: {
            folderDialog.open()
        }
    }

    SmallBtn {
        id: btn_open_vid
        x: 494
        width: 140
        height: 30
        text: qsTr("Open video")
        anchors.right: parent.right
        anchors.top: parent.top
        btnIconSource: "images/svg_images/cil-movie.png"
        anchors.topMargin: 92
        anchors.rightMargin: 10
        onClicked: {
            con.openVideo()
        }
    }


    SmallBtn {
        id: btn_logs
        x: 494
        width: 140
        height: 30
        text: qsTr("Open logs")
        anchors.right: parent.right
        anchors.top: parent.top
        btnIconSource: "images/svg_images/cil-description.png"
        anchors.topMargin: 132
        anchors.rightMargin: 10
        onClicked: {
            con.openLog()
        }
    }


    ProgressBar {
        id: progressBar
        y: 172
        height: 12
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        layer.mipmap: false
        hoverEnabled: true
        enabled: true
        anchors.bottomMargin: 56
        anchors.rightMargin: 10
        anchors.leftMargin: 10
        objectName: "progressBar"


        background: Rectangle {
            implicitWidth: 200
            implicitHeight: 6
            color: "#829298"
        }

        contentItem: Item {
            implicitWidth: 200
            implicitHeight: 12

            Rectangle {
                width: progressBar.value * parent.width
                height: parent.height
                color: "#0CCA4A"
            }
        }
    }

    MainBtn {
        id: btn_analyze
        y: 190
        height: 40

        text: qsTr("Start analyze")
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.rightMargin: 10
        objectName: "btn_analyze"

        enabled: true

        onClicked: {
            con.startAnalyze()
        }
    }

    FileDialog {
        id: fileDialog
        title: "Please choose a file"
        folder: "./"
        nameFilters: [ "Video files (*.mp4 *.avi)" ]
        onAccepted: {
            txt_source.text = con.getSourceVid(fileDialog.fileUrl)
            console.log("You chose: " + fileDialog.fileUrl)
        }
        onRejected: {
            console.log("Canceled")
        }
    }

    FileDialog {
        id: folderDialog
        title: "Please choose a folder"
        folder: "./"
        selectFolder: true

        onAccepted: {
            txt_destination.text = con.getDestFolder(folderDialog.fileUrl)
            console.log("You chose: " + folderDialog.fileUrl)
        }
        onRejected: {
            console.log("Canceled")
        }
    }

    Popup {
        id: popup_warning
        anchors.centerIn: parent
        modal: true
        focus: true
        padding: 10
        background: Rectangle {
            color: "#1c1d20"
        }

        contentItem: Text {
            color: "#ffffff"
            text: "You must select source file and destination path first"
        }

        objectName: "popup_warning"
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }

    Popup {
        id: popup_not_found
        anchors.centerIn: parent
        modal: true
        focus: true
        padding: 10
        background: Rectangle {
            color: "#1c1d20"
        }

        contentItem: Text {
            color: "#ffffff"
            text: "No output video/log file found. You must analyse something first"
        }

        objectName: "popup_not_found"
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }

    Popup {
        id: popup_success
        anchors.centerIn: parent
        modal: true
        focus: true
        padding: 10
        background: Rectangle {
            color: "#1c1d20"
        }

        contentItem: Text {
            color: "#ffffff"
            text: "Video analysed successfully"
        }

        objectName: "popup_success"
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }

    Popup {
        id: popup_error
        anchors.centerIn: parent
        modal: true
        focus: true
        padding: 10
        background: Rectangle {
            color: "#1c1d20"
        }

        contentItem: Text {
            color: "#ffffff"
            text: "Error occurred! Please restart program"
        }

        objectName: "popup_error"
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }

    Popup {
        id: popup_wait
        anchors.centerIn: parent
        modal: true
        focus: true
        padding: 10
        background: Rectangle {
            color: "#1c1d20"
        }

        contentItem: Text {
            color: "#ffffff"
            text: "You must wait"
        }

        objectName: "popup_wait"
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.8999999761581421}
}
##^##*/

import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: mainBtn
    text: qsTr("Main BTN")

    // CUSTOM PROPERTIES
    property url btnIconSource: "../../images/svg_images/cil-media-play.png"
    property color btnColorDefault: "#1c1d20"
    property color btnColorMouseOver: "#23272E"
    property color btnColorClicked: "#00a1f1"
    property int iconWidth: 18
    property int iconHeight: 18
    property color activeMenuColor: "#55aaff"
    property color activeMenuColorRight: "#2c313c"
    property bool isActiveMenu: false
    width: 780
    height: 40

    QtObject{
        id: internal

        // MOUSE OVER AND CLICK CHANGE COLOR
        property var dynamicColor: if(mainBtn.down){
                                       mainBtn.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       mainBtn.hovered ? btnColorMouseOver : btnColorDefault
                                   }

    }

    implicitWidth: 780
    implicitHeight: 40

    background: Rectangle{
        id: bgBtn
        color: internal.dynamicColor

        Rectangle{
            anchors{
                top: parent.top
                left: parent.left
                bottom: parent.bottom
            }
            color: activeMenuColor
            width: 3
            visible: isActiveMenu
        }

        Rectangle{
            anchors{
                top: parent.top
                right: parent.right
                bottom: parent.bottom
            }
            color: activeMenuColorRight
            width: 5
            visible: isActiveMenu
        }

    }

    contentItem: Item{
        clip: false
        anchors.horizontalCenter: parent.horizontalCenter
        id: content
        width: 780
        visible: true
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.topMargin: 0
        Image {
            id: iconBtn
            source: btnIconSource
            anchors.horizontalCenterOffset: -50
            anchors.horizontalCenter: parent.horizontalCenter
            //anchors.leftMargin: 26
            anchors.verticalCenter: parent.verticalCenter
            sourceSize.width: iconWidth
            sourceSize.height: iconHeight
            width: iconWidth
            height: iconHeight
            fillMode: Image.PreserveAspectFit
            visible: true
            antialiasing: true
        }

        ColorOverlay{
            source: iconBtn
            anchors.horizontalCenterOffset: -50
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.bottomMargin: 21
            color: "#ffffff"
            anchors.verticalCenter: parent.verticalCenter
            anchors.bottom: parent.bottom
            antialiasing: true
            width: iconWidth
            height: iconHeight
        }

        Text{
            color: "#ffffff"
            text: mainBtn.text
            font: mainBtn.font
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenterOffset: 0
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}


import QtQuick 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.15

Button{
    id: btnLeftMenu
    text: qsTr("Left Menu Text")

    // CUSTOM PROPERTIES
    property url btnIconSource: "../../images/svg_images/cil-file.png"
    property color btnColorDefault: "#1c1d20"
    property color btnColorMouseOver: "#23272E"
    property color btnColorClicked: "#00a1f1"
    property int iconWidth: 18
    property int iconHeight: 18
    property color activeMenuColor: "#55aaff"
    property color activeMenuColorRight: "#2c313c"
    property bool isActiveMenu: false

    QtObject{
        id: internal

        // MOUSE OVER AND CLICK CHANGE COLOR
        property var dynamicColor: if(btnLeftMenu.down){
                                       btnLeftMenu.down ? btnColorClicked : btnColorDefault
                                   } else {
                                       btnLeftMenu.hovered ? btnColorMouseOver : btnColorDefault
                                   }

    }

    implicitWidth: 250
    implicitHeight: 60

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
        anchors.horizontalCenter: parent.horizontalCenter
        id: content
        width: 140
        height: 30
        anchors.verticalCenter: parent.verticalCenter
        anchors.top: parent.top
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
            visible: false
            antialiasing: true
        }

        ColorOverlay{
            source: iconBtn
            anchors.horizontalCenterOffset: -45
            anchors.horizontalCenter: parent.horizontalCenter
            color: "#ffffff"
            anchors.verticalCenter: parent.verticalCenter
            antialiasing: true
            width: iconWidth
            height: iconHeight
        }

        Text{
            color: "#ffffff"
            text: btnLeftMenu.text
            font: btnLeftMenu.font
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenterOffset: 15
            anchors.horizontalCenter: parent.horizontalCenter
        }
    }
}
/*##^##
Designer {
    D{i:0;autoSize:true;height:60;width:250}
}
##^##*/

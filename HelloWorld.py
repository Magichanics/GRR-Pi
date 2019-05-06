import sys

from javafx.application import Application

class HelloWorld(Application):

    @classmethod
    def main(cls, args):
        HelloWorld.launch(cls, args)

    def start(self, primaryStage):
        primaryStage.setTitle('Hello World!')

        from javafx.scene import Scene
        from javafx.scene.layout import StackPane
        primaryStage.setScene(Scene(StackPane(), 320, 240))
        primaryStage.show()

if __name__ == '__main__':
    HelloWorld.main(sys.argv)
package application;
	
import javafx.application.Application;
import javafx.stage.Stage;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;

import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Paths;

import org.python.core.PyObject;
import org.python.util.PythonInterpreter;



public class Main extends Application {
	
	@FXML private Button btnDisplayMap;
	@FXML private ImageView imgMap;
	
	@Override
	public void start(Stage primaryStage) {
		try {
			//Load and display stage
			Parent root = FXMLLoader.load(getClass().getResource("GRRUI.fxml"));
			Scene scene = new Scene(root);
			//scene.getStylesheets().add(getClass().getResource("application.css").toExternalForm());
			primaryStage.setScene(scene);
			primaryStage.setTitle("Great Roaming Robot!");
			primaryStage.show();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	@FXML
	void displayMap() throws IOException
	{
		InputStream stream = Files.newInputStream(Paths.get("src/application/picmap.png"));
		imgMap.setImage(new Image(stream));
		//PythonInterpreter interpreter = new PythonInterpreter();
		//interpreter.exec("import sys\nsys.path.append('pathToModules if they are not there by default')\nimport yourModule");
		
		// execute a function that takes a string and returns a string
		//PyObject displayMap = interpreter.get("funcName");
		//PyObject result = someFunc.__call__(new PyString("Test!"));
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}

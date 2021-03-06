package nss.delta.agentmanager.targetcon;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.lang.reflect.Field;
import java.util.ArrayList;

public class Floodlight implements TargetController {
	private Process process = null;
	private boolean isRunning = false;

	public String version = "";
	public String controllerPath = "";
	public String appPath = "";

	private int currentPID = -1;

	private BufferedWriter stdIn;
	private BufferedReader stdOut;

	
	public Floodlight(String controllerPath, String version) {
		this.controllerPath = controllerPath;
		this.version = version;
	}

	public int createController() {
		isRunning = false;

		String str = "";
		try {
			process = Runtime.getRuntime().exec("java -jar " + controllerPath);

			Field pidField = Class.forName("java.lang.UNIXProcess").getDeclaredField("pid");
			pidField.setAccessible(true);
			Object value = pidField.get(process);

			this.currentPID = (int) value;

			try {
				Thread.sleep(7000);
			} catch (InterruptedException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			stdOut = new BufferedReader(new InputStreamReader(process.getInputStream()));
			stdIn = new BufferedWriter(new OutputStreamWriter(process.getOutputStream()));

			while ((str = stdOut.readLine()) != null) {
				// System.out.println(str);
				if (str.contains("Starting DebugServer on :6655")) {
					isRunning = true;
					break;
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (NoSuchFieldException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (SecurityException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (ClassNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (IllegalArgumentException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		} catch (IllegalAccessException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}

		return currentPID;
	}

	public Process getProc() {
		return this.process;
	}

	public void killController() {
		Process pc = null;
		try {
			if (process != null) {
				process.getErrorStream().close();
				process.getInputStream().close();
				process.getOutputStream().close();
			}

			pc = Runtime.getRuntime().exec("kill -9 " + this.currentPID);
			pc.getErrorStream().close();
			pc.getInputStream().close();
			pc.getOutputStream().close();
			pc.waitFor();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.currentPID = -1;
	}

	/*
	 * In the case of Floodlight, App-Agent is automatically installed when the
	 * controller starts
	 */
	public boolean installAppAgent() {

		return true;
	}

	@Override
	public String getType() {
		// TODO Auto-generated method stub
		return "Floodlight";
	}
	
	@Override
	public String getVersion() {
		// TODO Auto-generated method stub
		return this.version;
	}
	
	@Override
	public String getPath() {
		// TODO Auto-generated method stub
		return this.controllerPath;
	}


	@Override
	public int getPID() {
		// TODO Auto-generated method stub
		return this.currentPID;
	}
}

package nss.delta.agentmanager.core;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;

public class Configuration {
	private String FLOODLIGHT_ROOT = "";
	private String FLOODLIGHT_VER = "";
	
	private String ODL_ROOT = "";
	private String ODL_VER = "";
	private String ODL_APPAGENT = "";
	
	private String ONOS_ROOT = "";
	private String ONOS_VER = "";
	private String ONOS_KARAF_ROOT = "";
	
	private String CBENCH_ROOT = "";
	private String TARGET_CONTROLLER = "";
	private String OF_PORT = "";
	private String OF_VERSION = "";
	private String SWITCH_IP = "";
	private String MITM_NIC = "";
	private String CONTROLLER_IP = "";
	
	private String original = "";
	
	public Configuration (String file) {
		this.readConfigFile(file);
	}
	
	public String getFloodlightRoot() {
		return this.FLOODLIGHT_ROOT;
	}
	
	public String getFloodlightVer() {
		return this.FLOODLIGHT_VER;
	}
	
	public String getODLRoot() {
		return this.ODL_ROOT;
	}
	
	public String getODLVer() {
		return this.ODL_VER;
	}
	
	public String getODLAppAgent() {
		return this.ODL_APPAGENT;
	}
	
	public String getONOSRoot() {
		return this.ONOS_ROOT;
	}
	
	public String getONOSVer() {
		return this.ONOS_VER;
	}
	
	public String getONOSKarafRoot() {
		return this.ONOS_KARAF_ROOT;
	}
	
	public String getCbenchRoot() {
		return this.CBENCH_ROOT;
	}
	
	public String getTargetController() {
		return this.TARGET_CONTROLLER;
	}
	
	public String getOFPort() {
		return this.OF_PORT;
	}
	
	public String getOFVer() {
		return this.OF_VERSION;
	}
	
	public String getMitmNIC() {
		return this.MITM_NIC;
	}
	
	public String getControllerIP() {
		return this.CONTROLLER_IP;
	}
	
	public String getSwitchIP() {
		return this.SWITCH_IP;
	}
	
	public String show() {		
		return original;		
	}	
	
	public void readConfigFile(String config) {
		BufferedReader br = null;
		InputStreamReader isr = null;
		FileInputStream fis = null;
		File file = new File(config);
		String temp = "";

		try {
			fis = new FileInputStream(file);
			isr = new InputStreamReader(fis, "UTF-8");
			br = new BufferedReader(isr);

			while ((temp = br.readLine()) != null) {
				
				original += temp+"\n";
				
				if (temp.contains("FLOODLIGHT_ROOT")) 
					this.FLOODLIGHT_ROOT = temp.substring(temp.indexOf("=") + 1);				
				if (temp.contains("FLOODLIGHT_VER")) 
					this.FLOODLIGHT_VER = temp.substring(temp.indexOf("=") + 1);
				
				if (temp.contains("ODL_ROOT")) 
					this.ODL_ROOT = temp.substring(temp.indexOf("=") + 1);				
				if (temp.contains("ODL_VER")) 
					this.ODL_VER = temp.substring(temp.indexOf("=") + 1);
				if (temp.contains("ODL_APPAGENT")) 
					this.ODL_APPAGENT = temp.substring(temp.indexOf("=") + 1);

				if (temp.contains("ONOS_ROOT")) 
					this.ONOS_ROOT = temp.substring(temp.indexOf("=") + 1);
				if (temp.contains("ONOS_VER")) 
					this.ONOS_VER = temp.substring(temp.indexOf("=") + 1);
				if (temp.contains("ONOS_KARAF_ROOT")) 
					this.ONOS_KARAF_ROOT = temp.substring(temp.indexOf("=") + 1);

				if (temp.contains("CBENCH_ROOT")) 
					this.CBENCH_ROOT = temp.substring(temp.indexOf("=") + 1);

				if (temp.contains("TARGET_CONTROLLER")) 
					this.TARGET_CONTROLLER = temp.substring(temp.indexOf("=") + 1);

				if (temp.contains("OF_PORT")) 
					this.OF_PORT = temp.substring(temp.indexOf("=") + 1);
				if (temp.contains("OF_VERSION")) 
					this.OF_VERSION = temp.substring(temp.indexOf("=") + 1);
				
				if (temp.contains("SWITCH_IP")) 
					this.SWITCH_IP = temp.substring(temp.indexOf("=") + 1);
				if (temp.contains("CONTROLLER_IP")) 
					this.CONTROLLER_IP = temp.substring(temp.indexOf("=") + 1);
				
				if (temp.contains("MITM_NIC")) 
					this.MITM_NIC = temp.substring(temp.indexOf("=") + 1);			
			}

		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				fis.close();
				isr.close();
				br.close();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}

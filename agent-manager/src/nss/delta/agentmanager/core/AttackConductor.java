package nss.delta.agentmanager.core;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.*;
import java.io.IOException;
import java.net.Socket;
import java.util.HashMap;
import java.util.Iterator;
import java.util.TreeMap;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import nss.delta.agentmanager.targetcon.ControllerManager;
import nss.delta.agentmanager.testcase.TestAdvancedCase;
//CHANGE HERE
import nss.delta.agentmanager.testcase.LayerTwoTestAdvancedCase;
import nss.delta.agentmanager.testcase.TestInfo;
import nss.delta.agentmanager.testcase.TestSwitchCase;
import nss.delta.agentmanager.utils.ProgressBar;

public class AttackConductor {
	private static final Logger log = LoggerFactory.getLogger(AttackConductor.class);

	public static final int UMODE_DEFAULT_COUNT = 100;

	private HashMap<String, String> infoSwitchCase;
	private HashMap<String, String> infoControllerCase;
	private HashMap<String, String> infoAdvancedCase;

	private AppAgentManager appm;
	private HostAgentManager hostm;
	private ChannelAgentManager channelm;
	private ControllerManager controllerm;
//CHANGE HERE
        private LayerTwoHostAgentManager layer2Hostm;

	private Configuration cfg;

	private DataOutputStream dos;
	private DataInputStream dis;
	private BufferedReader inReader;
	private PrintWriter outWriter;

	private TestAdvancedCase testAdvancedCase;
//CHANGE HERE
	private LayerTwoTestAdvancedCase layerTwoTestAdvancedCase;
	private TestSwitchCase testSwitchCase;

	public AttackConductor(String config) {
		infoControllerCase = new HashMap<String, String>();
		infoSwitchCase = new HashMap<String, String>();
		infoAdvancedCase = new HashMap<String, String>();

		cfg = new Configuration(config);

		this.controllerm = new ControllerManager(cfg);

		this.appm = new AppAgentManager();
		this.appm.setControllerType(cfg.getTargetController());

		this.hostm = new HostAgentManager();
		this.channelm = new ChannelAgentManager();
//CHANGE HERE
                this.layer2Hostm = new LayerTwoHostAgentManager();

		/* Update Test Cases */
		TestInfo.updateAdvancedCase(infoAdvancedCase);
		TestInfo.updateControllerCase(infoControllerCase);
		TestInfo.updateSwitchCase(infoSwitchCase);

		testAdvancedCase = new TestAdvancedCase(appm, hostm, channelm, controllerm);
//CHANGE HERE
		layerTwoTestAdvancedCase = new LayerTwoTestAdvancedCase(layer2Hostm);
		testSwitchCase = new TestSwitchCase();
	}

	public String showConfig() {
		return cfg.show();
	}

	public void setSocket(Socket socket) throws IOException {
		
		dos = new DataOutputStream(socket.getOutputStream());
		dis = new DataInputStream(socket.getInputStream());
		
		String agentType = dis.readUTF();//inReader.readLine();//dis.readUTF();
		
		if (agentType.contains("AppAgent")) {
			appm.setAppSocket(socket, dos, dis);
		} else if (agentType.contains("ActAgent")) { /* for OpenDaylight */
			appm.setActSocket(socket, dos, dis);
		} else if (agentType.contains("ChannelAgent")) {
			channelm.setSocket(socket, dos, dis);
			/* OFVersion + NIC + OFPort + Controller IP + Switch IP */
			channelm.write("config," + "version:" + cfg.getOFVer() + ",nic:" + cfg.getMitmNIC() + ",port:"
					+ cfg.getOFPort() + ",controller_ip:" + cfg.getControllerIP() + ",switch_ip:" + cfg.getSwitchIP());

		} 
		else if (agentType.contains("L2HostAgent")) {
			//CHANGE HERE
			layer2Hostm.setSocket(socket, dos, dis);

		}else if (agentType.contains("HostAgent")) {
			hostm.setSocket(socket, dos, dis);			
		}
	}

	public void replayKnownAttack(String code) {
		if (code.charAt(0) == '1')
			testSwitchCase.replayKnownAttack(code);
		if (code.charAt(0) == '3')
			testAdvancedCase.replayKnownAttack(code);
	}

//CHANGE HERE
	public String generateFlow(String code) {
		return layerTwoTestAdvancedCase.generateFlow(code);
	}

	public void printAttackList() {
		System.out.println("\nControl Plane Test Set");

		Iterator<String> treeMapIter = infoControllerCase.keySet().iterator();

		while (treeMapIter.hasNext()) {

			String key = treeMapIter.next();
			String value = infoControllerCase.get(key);
			System.out.println(String.format("%s\t: %s", key, value));
		}

		System.out.println("\nData Plane Test Set");
		treeMapIter = infoSwitchCase.keySet().iterator();

		while (treeMapIter.hasNext()) {

			String key = treeMapIter.next();
			String value = infoSwitchCase.get(key);
			System.out.println(String.format("%s\t: %s", key, value));
		}

		System.out.println("\nAdvanced Test Set");

		TreeMap<String, String> treeMap = new TreeMap<String, String>(infoAdvancedCase);
		treeMapIter = treeMap.keySet().iterator();
		while (treeMapIter.hasNext()) {

			String key = (String) treeMapIter.next();
			String value = (String) treeMap.get(key);
			System.out.println(String.format("%s\t: %s", key, value));
		}
	}

	public boolean isPossibleAttack(String code) {
		if (infoControllerCase.containsKey(code))
			return true;
		else if (infoSwitchCase.containsKey(code))
			return true;
		else if (infoAdvancedCase.containsKey(code))
			return true;
		else
			return false;
	}

	public void test(String code) {
		this.appm.write(code);
	}

	public void replayAllKnownAttacks() {

	}
}

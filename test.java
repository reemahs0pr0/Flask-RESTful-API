package test;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

public class test {

	public static void main(String[] args) {
		
		  try { 
			  // personalised main page
			  int userId = 1;
			  URL url = new URL("http://127.0.0.1:5000/?id=" + userId);
			  
			  // search results
//			  String keyword = "software developer";
//			  String keywordParam = keyword.replace(" ", "+");
//			  URL url = new URL("http://127.0.0.1:5000/search/?query=" + keywordParam); 
			  
			  HttpURLConnection conn = (HttpURLConnection) url.openConnection();
			  
			  conn.setRequestMethod("GET");
		      conn.connect();
		      BufferedReader rd  = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		      StringBuilder sb = new StringBuilder();
		      String line = null;
	          while ((line = rd.readLine()) != null)
	          {
	              sb.append(line + '\n');
	          }
	          rd.close();
	          conn.disconnect();
	          
	          String[] arr = sb.toString().split(",");
	          List<Integer> list = new ArrayList<>();
	          for (int i = 0; i < arr.length-1; i++) {
	        	  list.add(Integer.parseInt(arr[i]));
	          }
	          System.out.println(list);
		  }
		  catch (Exception e) {
	            e.printStackTrace();
	      }
	}
}

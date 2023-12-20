// Source code is decompiled from a .class file using FernFlower decompiler.
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;

public class another {
   public void nite() {
   }

   public static String convertString(String var0) {
      ArrayList var1 = new ArrayList();
      char[] var2 = var0.toCharArray();
      int var3 = var2.length;

      int var4;
      int var5;
      for(var4 = 0; var4 < var3; ++var4) {
         var5 = var2[var4];
         var1.add(Character.valueOf((char)var5));
      }

      Collections.shuffle(var1);
      HashMap var9 = new HashMap();
      char[] var10 = var0.toCharArray();
      var4 = var10.length;

      int var6;
      for(var5 = 0; var5 < var4; ++var5) {
         var6 = var10[var5];
         var9.put(Character.valueOf((char)var6), (Character)var1.remove(0));
      }

      StringBuilder var11 = new StringBuilder();
      char[] var12 = var0.toCharArray();
      var5 = var12.length;

      for(var6 = 0; var6 < var5; ++var6) {
         char var7 = var12[var6];
         char var8 = (Character)var9.getOrDefault(var7, var7);
         var11.append(var8);
      }

      return var11.toString();
   }

   private static String convert(String var0) {
      StringBuilder var1 = new StringBuilder();

      for(int var2 = 0; var2 < var0.length(); var2 += 2) {
         String var3 = var0.substring(var2, var2 + 2);
         int var4 = Integer.parseInt(var3, 16);
         var1.append((char)var4);
      }

      return var1.toString();
   }

   public static void main(String[] var0) {
      String var1 = "686d6d5f6c34793372355f";
      String var2 = "76335f7734795f3730305f6d346e79";
      String var3 = "6e6974657b315f6834";
      String var4 = "5f64306c6c355f6e30775f";
      String var5 = "30665f6c3166335f69677d";
      String var6 = convert(var3 + var2 + var4 + var1 + var5);
      System.out.println(var6);
      String var7 = convertString(var6);
      System.out.println("1_h4t3_str1ng_m4n1pul4710n_1n_java: " + var7);
   }
}

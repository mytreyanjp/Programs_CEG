import java.util.Scanner;
import java.util.ArrayList;
import java.util.Arrays;

class Currency{
    public int id;
    String name;
    String symbol;
    double exchangerate;

    Currency(int i,String n, String s, double e){
        id=i;name=n; symbol=s; exchangerate=e;
    }

    public String toString(){
        String a= "Country: "+name+" with a exchange rate of 1$ = "+exchangerate+" "+symbol;
        return a;
    }
}
public class CurrencyManager{
    ArrayList<Currency> curr= new ArrayList<>();

    public void addcurrency(int i,String n,String s,double e){
        Currency c=new Currency(i,n,s,e);
        curr.add(c);

    }

    public void retrievecurrency(String n){

        for(Currency c: curr){
            if(c.name==n){
                System.out.println(n+ " -Currency is "+c.symbol);
                c.id+=1;
            }

        }
    }
    ArrayList<Currency> getCurrencies(String n){
        ArrayList<Currency> newlist=new ArrayList<>();
        for(Currency c: curr){
            if(c.name==n){
                newlist.add(c);
                c.id+=1;
            }
        }
        return newlist;
    }
    ArrayList<Currency> getCurrencies(double e){
        ArrayList<Currency> newlist=new ArrayList<>();
        for(Currency c: curr){
            if(c.exchangerate==e){
                newlist.add(c);
                c.id+=1;
            }
        }
        return newlist;
    }
    ArrayList<Currency> getCurrencies(String n,double e){
        ArrayList<Currency> newlist=new ArrayList<>();
        for(Currency c: curr){
            if(c.exchangerate==e && c.name==n){
                newlist.add(c);
                c.id+=1;
            }
        }
        return newlist;
    }
    
    void Frequency(){
        System.out.println("Frequency:");
        for(Currency c: curr){
            System.out.println(c.name+":"+c.id);
        }
    }
    

 public static void main(String args[]){
    CurrencyManager manager=new CurrencyManager();
    
    manager.addcurrency(0,"India","Rupee",0.23);
    manager.addcurrency(0,"Japan","Yen",0.08);
    manager.addcurrency(0,"Dubai","Dhiraam",0.63);
    manager.addcurrency(0,"China","Yuan",0.37);
    manager.addcurrency(0,"Europe","Euro",1.63);

  
    manager.retrievecurrency("Japan");
    manager.retrievecurrency("India");
    manager.retrievecurrency("China");



    ArrayList<Currency> name=new ArrayList<>();
    name=manager.getCurrencies("Dubai");
    for(Currency c:name){
        System.out.println(c.toString());
    }

    ArrayList<Currency> rate=new ArrayList<>();
    rate=manager.getCurrencies(0.37);
    for(Currency c:rate){
        System.out.println(c.toString());
    }

    ArrayList<Currency> nameandrate=new ArrayList<>();
    nameandrate=manager.getCurrencies("India",0.23);
    for(Currency c:nameandrate){
        System.out.println(c.toString());
    }
    manager.Frequency();

 }
}
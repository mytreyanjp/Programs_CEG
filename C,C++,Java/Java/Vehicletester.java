 import java.util.Random;

 abstract class Vehicle{
    private static int countv=0;
    protected String owner;
    protected final String regno;

    public Vehicle(String rno,String name){
        regno=rno;
        owner=name;
        countv++;
    }

    public static void displayc(){
        System.out.println("Number of vehicles: "+countv);
    }
    public final void displayr() {
        System.out.println("Registration Number: " + regno);
        System.out.println("Owner Name: " + owner);
    }
  
    abstract void startEngine();

}
class car extends Vehicle{

    public car(String registrationNumber,String ownerName) {
        super(registrationNumber,ownerName);
    }

    public void startEngine() {
        System.out.println("Car engine started");
    }
}
class bike extends Vehicle{
    public bike(String registrationNumber, String ownerName) {
        super(registrationNumber,ownerName);
    }


    public void startEngine() {
        System.out.println("Bike engine started");
    }
}

class truck extends Vehicle{
    public truck(String registrationNumber, String ownerName) {
        super(registrationNumber,ownerName);
    }

    public void startEngine() {
        System.out.println("Truck engine started");
    }
}

final class ElectricCar extends car {
    public ElectricCar(String registrationNumber, String ownerName) {
        super(registrationNumber,ownerName);
    }

    public void chargeBattery() {
        System.out.println("Battery charging...");
    }

    public void showBatteryStatus() {
        System.out.println("Battery: 54%");
    }
}
interface FuelEfficiency {
    void calculateFuelEfficiency();
}
class fuel implements FuelEfficiency{
    int distancetravelled;
    int fuelc;
    public fuel(int x,int y){
        distancetravelled=x;
        fuelc=y;
    }
    public void calculateFuelEfficiency(){
        System.out.println(distancetravelled/fuelc+"%");
    }

}

public class Vehicletester{
    public static void main(String[] args) {
        Random r=new Random();
        Vehicle[] vehicles = new Vehicle[4];
        vehicles[0] = new car("TG3455", "Alex");
        vehicles[1] = new bike("WD8199", "Jackson");
        vehicles[2] = new truck("RT4003", "Harris");
        vehicles[3] = new ElectricCar("QS2311", "Laila");

        for (Vehicle vehicle : vehicles) {
            vehicle.startEngine();
            vehicle.displayr();
            
            if(vehicle instanceof ElectricCar){
                ElectricCar vehiclee = (ElectricCar) vehicle;
                vehiclee.chargeBattery();
                vehiclee.showBatteryStatus();
                System.out.print("Battery Efficiency is: ");
            }
            else{
                System.out.print("Fuel Efficiency is: ");

            }
            fuel f=new fuel(r.nextInt(80)+20,r.nextInt(10)+1);
            f.calculateFuelEfficiency();
            System.out.println();
            
        }
        Vehicle.displayc();
 
    }
}

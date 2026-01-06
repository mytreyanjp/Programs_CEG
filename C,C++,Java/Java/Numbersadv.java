import java.util.Scanner;

 public class Numbersadv{
    int arr[]=new int[100];
    int c=0;
    void compare(int x,int size){
            arr[size-1]=x;
            c++;
            int sum=0,avg;
            int smallest=arr[0];
            int largest=arr[0];
            for(int i=0;i<c;i++){      
                if(arr[i]<smallest)
                    smallest=arr[i];
                if(arr[i]>largest)
                    largest=arr[i];
                sum+=arr[i];    
            }
            System.out.println("Largest:"+largest+"\nSmallest:"+smallest+"\nSum:"+sum+"\nAverage:"+sum/c);
        
    }
    public static void main(String[] args){
        Scanner s=new Scanner(System.in);
        Numbers n= new Numbers();
        int count=0;
        System.out.println("Enter -1 to exit:"); 
        while(true){
           System.out.print("\nEnter number-"+(count+1)+":");
           int a=s.nextInt();
           if(a==-1){
            break;
           }
           count++;
           n.compare(a,count); 
        }

        
    }
}
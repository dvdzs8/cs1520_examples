use std::fmt;

enum MyList<T> {
    // write code here
}

impl<T> MyList<T> {
    // Add three functions here, create (creates empty list), append, and len
}

impl<T: fmt::Display> fmt::Display for MyList<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        //write code here
    }
}

fn main() {
    //this should run without any errors

    let mut list = MyList::<i32>::create();
    list.append(10);
    list.append(20);
    list.append(30);
    list.append(40);
    list.append(50);
    println!("{}", list);
    println!("List Lenght :: {}", list.len());
}

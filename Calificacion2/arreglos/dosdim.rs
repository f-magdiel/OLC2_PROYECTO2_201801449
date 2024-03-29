fn llenarMat(a: &mut [[i64; 3]; 3], b: &mut [[i64; 3]; 3]) {
    for i in 0..a.len() {
        for j in 0..a.len() {
            a[i][j] = (i as i64) * 3 + (j as i64);
            b[i][j] = i64::pow((i as i64), 3) - i64::pow((j as i64), 2) + 10;
        }
    }
}

fn sumarMat(a: &mut [[i64; 3]; 3], b: &mut [[i64; 3]; 3], r: &mut [[i64; 3]; 3]) {
    for i in 0..3 {
        for j in 0..3 {
            r[i][j] = a[i][j] + b[i][j];
        }
    }
}

fn restarMat(a: &mut [[i64; 3]; 3], b: &mut [[i64; 3]; 3], r: &mut [[i64; 3]; 3]) {
    for i in 0..3 {
        for j in 0..3 {
            r[i][j] = a[i][j] - b[i][j];
        }
    }
}

fn multMat(a: &mut [[i64; 3]; 3], b: &mut [[i64; 3]; 3], r: &mut [[i64; 3]; 3]) {
    for i in 0..3 {
        for j in 0..3 {
            for k in 0..3 {
                r[i][j] = r[i][j] + a[i][k] * b[k][j];
            }
        }
    }
}

fn limpiarMat(a: &mut [[i64; 3]; 3]) {
    for i in 0..3 {
        for j in 0..3 {
            a[i][j] = 0;
        }
    }
}

fn printMat(r: &mut [[i64; 3]; 3]) {
    for i in 0..r.len() {
        println!("{:?}", r[i]);
    }
}

fn main() {
    let mut matA: [[i64; 3]; 3] = [[0,0,0],[0,0,0],[0,0,0]];
    let mut matB: [[i64; 3]; 3] = [[0,0,0],[0,0,0],[0,0,0]];
    let mut matR: [[i64; 3]; 3] = [[0,0,0],[0,0,0],[0,0,0]];

    // llenar matriz
    llenarMat(&mut matA, &mut matB);

    println!("Matriz A");
    printMat(&mut matA);
    println!("");
    println!("Matriz B");
    printMat(&mut matB);
    println!("");
    println!("Matriz R");
    printMat(&mut matR);
    println!("");

    // sumar matriz
    sumarMat(&mut matA, &mut matB, &mut matR);
    println!("R = A + B");
    printMat(&mut matR);
    println!("");

    // restar matriz
    limpiarMat(&mut matR);
    restarMat(&mut matB, &mut matA, &mut matR);
    println!("R = B - A");
    printMat(&mut matR);
    println!("");

    // multiplicar matriz
    limpiarMat(&mut matR);
    multMat(&mut matA, &mut matB, &mut matR);
    println!("R = A * B");
    printMat(&mut matR);
    println!("");
}
/*
Matriz A
[0, 1, 2]
[3, 4, 5]
[6, 7, 8]

Matriz B
[10, 9, 6]
[11, 10, 7]
[18, 17, 14]

Matriz R
[0, 0, 0]
[0, 0, 0]
[0, 0, 0]

R = A + B
[10, 10, 8]
[14, 14, 12]
[24, 24, 22]

R = B - A
[10, 8, 4]
[8, 6, 2]
[12, 10, 6]

R = A * B
[47, 44, 35]
[164, 152, 116]
[281, 260, 197]
*/
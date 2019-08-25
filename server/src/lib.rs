#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
use rocket::http::RawStr;


#[post("/auth?<code>&<state>")]
fn index(code: &RawStr, state: &RawStr) -> String {
    // ok to unwrap, from the rocket documentation:
    // "Note: Rocket should never hand you a bad `&RawStr`."
    println!("{}", code);
    println!("{}", state);
    code.url_decode().unwrap()
}

#[get("/")]
fn index_get() -> String {
    "hello".to_string()
}

pub fn rocket() -> rocket::Rocket {
    rocket::ignite().mount("/", routes![index, index_get])
}

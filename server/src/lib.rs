#![feature(proc_macro_hygiene, decl_macro)]

#[macro_use] extern crate rocket;
use rocket::http::{RawStr, Status};
use rocket::request::{FromRequest, Outcome, Request};

use postgres::{Connection, TlsMode};


#[post("/auth?<code>&<state>")]
fn index(code: &RawStr, state: &RawStr) -> String {
    // ok to unwrap, from the rocket documentation:
    // "Note: Rocket should never hand you a bad `&RawStr`."
    println!("{}", code);
    println!("{}", state);
    code.url_decode().unwrap()
}

struct TokenRepo;
impl TokenRepository for TokenRepo {
    fn token_exists(&self, tok: &str) -> bool {
        let conn = Connection::connect("postgres://tyler@localhost/staccato-dev", TlsMode::None).unwrap();
        let res = conn.query("select 1 from auth_token where token = $1", &[&tok]).unwrap();
        // i think the connection is closed automatically, the InnerConnection in the library
        // is stored in a RefCell
        !res.is_empty()
    }
}
trait TokenRepository {
    fn token_exists(&self, tok: &str) -> bool;
}


#[derive(Debug)]
enum AuthTokenError {
    Missing,
    Incorrect
}

struct AuthToken(String);
impl<'a, 'r> FromRequest<'a, 'r> for AuthToken {
    type Error = AuthTokenError;

    fn from_request(request: &'a Request<'r>) -> Outcome<Self, Self::Error> {
        let header: Vec<_> = request.headers().get("Authorization").collect();
        match header.len() {
            1 => {
                let split: Vec<_> = header[0].split(" ").collect();
                match split.len() {
                    2 => {
                        let repo = TokenRepo {};
                        if repo.token_exists(split[1]) {
                            return Outcome::Success(AuthToken(String::from(split[1])));
                        }
                        Outcome::Failure((Status::BadRequest, AuthTokenError::Incorrect))
                    }
                    0 | 1 | _ => Outcome::Failure((Status::BadRequest, AuthTokenError::Missing)),
                }
            },
            _ => Outcome::Failure((Status::BadRequest, AuthTokenError::Missing))
        }
    }
}

#[get("/")]
fn index_get(token: AuthToken) -> String {
    token.0
}

pub fn rocket() -> rocket::Rocket {
    rocket::ignite().mount("/", routes![index, index_get])
}

use staccato::rocket;
use rocket::local::Client;
use rocket::http::{Header, Status};


#[cfg(test)]
mod integration_tests {

    use super::*;

    fn setup_client() -> Client{
        let rocket_inst = rocket();
        Client::new(rocket_inst).expect("valid rocket instance")
    }

    #[test]
    fn smoke_test() {
        let client = setup_client();
        let req = client.get("/");
        let mut res = req.dispatch();
        assert_eq!(res.body_string().unwrap(), "hello");
    }

    #[test]
    fn test_missing_authorization_header_results_in_bad_request() {
        let client = setup_client();
        let req = client.get("/");
        let res = req.dispatch();
        assert_eq!(res.status(), Status::BadRequest);
    }

    #[test]
    fn test_incorrect_authorization_header_results_in_bad_request() {
        let client = setup_client();
        let header = Header::new("Authorization", "Bearer incorrect");
        let mut req = client.get("/");
        req.add_header(header);
        let res = req.dispatch();
        assert_eq!(res.status(), Status::BadRequest);
    }

    #[test]
    fn test_correct_authorization_header_results_in_ok() {
        let client = setup_client();
        // TODO insert token into database
        let header = Header::new("Authorization", "Bearer incorrect");
        let mut req = client.get("/");
        req.add_header(header);
        let res = req.dispatch();
        assert_eq!(res.status(), Status::Ok);
    }
}

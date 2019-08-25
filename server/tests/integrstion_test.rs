use staccato::rocket;
use rocket::local::Client;


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
        unimplemented!();
    }
}

const faker = require("faker");

const randomEmail = faker.internet.email();

const logIn = () => {
    const { email, password } = Cypress.env("credentials");

    // Capture HTTP requests.
    cy.server();
    cy.route({
        method: "POST",
        url: "**/api/account/login**"
    }).as("logIn");

    // Log into the app.
    cy.visit("/#/login");
    cy.get("input#email").type(randomEmail);
    cy.get("input#password").type(password, { log: false });
    cy.get("button").contains("Anmelden").click();
    cy.wait("@logIn");
};

describe("Authentication", function () {
    it("Can sign up.", function () {
        cy.server();
        cy.route({
            method: "POST",
            url: "**/api/signup**"
        }).as("signUp");

        cy.visit("/#/signup");
        cy.get("input#email").type(randomEmail);
        cy.get("input#fullName").type("Gary Cole");
        cy.get("input#password").type("pAssw0rd", { log: false });

        cy.get("button").contains("Registrieren").click();
        cy.wait("@signUp");
        cy.hash().should("eq", "#/login");
    });
    it("Can log in.", function () {
        logIn();
        cy.hash().should("eq", "#/");
        cy.get("button").contains("Abmelden");
    });

    it("Cannot visit the login page when logged in.", function () {
        logIn();
        cy.visit("/#/login");
        cy.hash().should("eq", "#/");
    });

    it("Cannot see links when logged in.", function () {
        logIn();
        cy.get("button#signUp").should("not.exist");
        cy.get("button#logIn").should("not.exist");
    });

    it("Cannot visit the sign up page when logged in.", function () {
        logIn();
        cy.visit("/#/signup");
        cy.hash().should("eq", "#/");
    });
    it("Can log out.", function () {
        logIn();
        cy.get("button")
            .contains("Abmelden")
            .click()
            .should(() => {
                expect(window.localStorage.getItem("homework.checker.auth")).to
                    .be.null;
            });
        cy.get("button").contains("Abmelden").should("not.exist");
    });
    it("Show invalid fields on sign up error.", function () {
        cy.server();
        cy.route({
            method: "POST",
            url: "**/api/signup**",
            status: 400,
            response: {
                email: ["A user with that username already exists."]
            }
        }).as("signUp");
        cy.visit("/#/signup");
        cy.get("input#email").type(randomEmail);
        cy.get("input#fullName").type("Gary Cole");
        cy.get("input#password").type("pAssw0rd", { log: false });

        cy.get("button").contains("Registrieren").click();
        cy.wait("@signUp");
        cy.get("div.invalid-feedback").contains(
            "A user with that username already exists"
        );
        cy.hash().should("eq", "#/signup");
    });
    it("Shows an alert on login error.", function () {
        const { email, password } = Cypress.env("credentials");
        cy.server();
        cy.route({
            method: "POST",
            url: "**/api/login**",
            status: 400,
            response: {
                detail: "No active account found with the given credentials"
            }
        }).as("logIn");
        cy.visit("/#/login");
        cy.get("input#email").type(randomEmail);
        cy.get("input#password").type(password, { log: false });
        cy.get("button").contains("Anmelden").click();
        cy.wait("@logIn");
        cy.get("div.alert").contains(
            "No active account found with the given credentials"
        );
        cy.hash().should("eq", "#/login");
    });
});

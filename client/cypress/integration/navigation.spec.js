describe("Navigation", function () {
    it("Can navigate to sign up from home", function () {
        cy.visit("/#/");
        cy.get("a").contains("Registrieren").click();
        cy.hash().should("eq", "#/signup");
    });

    it("Can navigate to log in from home", function () {
        cy.visit("/#/");
        cy.get("a").contains("Anmelden").click();
        cy.hash().should("eq", "#/login");
    });

    it("Can navigate to home from sign up", function () {
        cy.visit("/#/signup");
        cy.get("a").contains("Hauptseite").click();
        cy.hash().should("eq", "#/");
    });

    it("Can navigate to log in from sign up", function () {
        cy.visit("/#/signup");
        cy.get("a").contains("Anmelden").click();
        cy.hash().should("eq", "#/login");
    });

    it("Can navigate to home from log in", function () {
        cy.visit("/#/login");
        cy.get("a").contains("Hauptseite").click();
        cy.hash().should("eq", "#/");
    });

    it("Can navigate to sign up from log in", function () {
        cy.visit("/#/login");
        cy.get("a").contains("Registrier").click();
        cy.hash().should("eq", "#/signup");
    });
});

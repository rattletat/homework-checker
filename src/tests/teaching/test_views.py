class TestHomeView:
    def test_home_page_returns_correct_html(self):
        response = self.client.get("/")
        assert "pages/home.html" in (t.name for t in response.templates)

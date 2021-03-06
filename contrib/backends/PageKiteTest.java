import net.pagekite.lib.PageKiteAPI;

public class PageKiteTest {
    public static void main(String[] args) {
        String Whitelabel_TLD = "pagekite.me";

        PageKiteAPI.initWhitelabel(
            "PageKiteTest", 25, 25,
            PageKiteAPI.PK_WITH_DEFAULTS,
            0, Whitelabel_TLD);

        PageKiteAPI.addKite(
            "http", "KITE.pagekite.me", 0, "SECRET",
            "localhost", 80);

        PageKiteAPI.threadStart();
        PageKiteAPI.threadWait();
    }
}

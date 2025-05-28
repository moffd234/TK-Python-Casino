from unittest.mock import patch, call

from Application.Casino.Accounts.UserAccount import UserAccount
from Application.Casino.Games.Slots.Slots import Slots, get_spin, handle_spin, get_payout, main
from Application.Utils.ANSI_COLORS import ANSI_COLORS
from Tests.BaseTest import BaseTest, IOCONSOLE_PATH, SLOTS_FILE_PATH, SLOTS_CLASS_PATH, GAME_CLASS_PATH


class TestSlots(BaseTest):

    def setUp(self):
        super().setUp()
        self.game = Slots(self.account, self.manager)

    def run_and_assert(self, mock_payout, mock_print_spin, mock_get_spin,
                       mock_get_money_input, mock_continue, mock_print_welcome):
        self.game.run()

        mock_payout.assert_called_once()
        mock_print_spin.assert_called_once_with(mock_get_spin.return_value)
        mock_get_spin.assert_called_once()
        mock_get_money_input.assert_called_once()
        mock_print_welcome.assert_called_once()

        expected_call_count: int = 2
        actual_call_count: int = mock_continue.call_count

        self.assertEqual(expected_call_count, actual_call_count)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_welcome_message(self, mock_print):
        expected: str = r"""        
        Yb        dP 888888 88      dP""b8  dP"Yb  8b    d8 888888     888888  dP"Yb      .dP"Y8 88      dP"Yb  888888 .dP"Y8 
         Yb  db  dP  88__   88     dP   `" dP   Yb 88b  d88 88__         88   dP   Yb     `Ybo." 88     dP   Yb   88   `Ybo." 
          YbdPYbdP   88""   88  .o Yb      Yb   dP 88YbdP88 88""         88   Yb   dP     o.`Y8b 88  .o Yb   dP   88   o.`Y8b 
           YP  YP    888888 88ood8  YboodP  YbodP  88 YY 88 888888       88    YbodP      8bodP' 88ood8  YbodP    88   8bodP' 
           
           Rules:
                - 1. Enter a wager amount.
                - 2. Match three symbols on the pay line to win
                - 3. Payouts vary based on the symbols matched:
                     - Three 7s: Jackpot(10x)
                     - Three Bells: Big Win(5x)
                     - Three Bars: Medium Win (2x)
                     - Three Cherries: Small Win (1.5x)
                     - Any other combination: No Win (You lose your wager)
        """

        self.game.print_welcome_message()

        mock_print.assert_called_with(expected)

    def test_get_spin(self):
        expected_len: int = 3
        actual_len: int = len(get_spin())

        outcomes: set[str] = set()
        possibilities: list[str] = ["7️⃣", "🔔", "⬛", "🍒"]

        for _ in range(1000):
            outcomes.add(get_spin()[0])
            outcomes.add(get_spin()[1])
            outcomes.add(get_spin()[2])

        for sym in possibilities:
            self.assertIn(sym, outcomes)

        self.assertEqual(expected_len, actual_len)

    def test_handle_spin_no_win(self):
        syms: list[str] = ["🔔", "🔔", "⬛"]

        expected: float = 0
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_7_win(self):
        syms: list[str] = ["7️⃣", "7️⃣", "7️⃣"]

        expected: float = 10
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_bell_win(self):
        syms: list[str] = ["🔔", "🔔", "🔔"]

        expected: float = 5
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_bar_win(self):
        syms: list[str] = ["⬛", "⬛", "⬛"]

        expected: float = 2
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    def test_handle_spin_cherry_win(self):
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 1.5
        actual: float = handle_spin(syms)

        self.assertEqual(expected, actual)

    @patch(f"{SLOTS_FILE_PATH}.handle_spin")
    def test_get_payout_assert_mock_called(self, mock_handle_spin):
        spin: list[str] = ["🔔", "🔔", "⬛"]
        get_payout(10, spin)

        mock_handle_spin.assert_called_once_with(spin)

    def test_get_payout_none(self):
        expected: float = 0

        spin: list[str] = ["🔔", "🔔", "⬛"]
        actual: float = get_payout(10, spin)

        self.assertEqual(expected, actual)

    def test_get_payout_7_win(self):
        syms: list[str] = ["7️⃣", "7️⃣", "7️⃣"]

        expected: float = 100.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_bell_win(self):
        syms: list[str] = ["🔔", "🔔", "🔔"]

        expected: float = 50.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_bar_win(self):
        syms: list[str] = ["⬛", "⬛", "⬛"]

        expected: float = 20.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_cherry_win(self):
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 15.0
        actual: float = get_payout(10, syms)

        self.assertEqual(expected, actual)

    def test_get_payout_round_up(self):
        # There is no round down test as that shouldn't be able to occur
        syms: list[str] = ["🍒", "🍒", "🍒"]

        expected: float = 15.50
        actual: float = get_payout(10.33, syms)

        self.assertEqual(expected, actual)

    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_print_spin(self, mock_print):
        self.game.print_spin(["🍒", "🍒", "🍒"])

        expected_calls = [
            call("\n🎰 Spinning... 🎰\n"),
            call("┌───┬───┬───┐"),
            call("│ 🍒│ 🍒│ 🍒│"),
            call("└───┴───┴───┘\n"),
        ]

        # Only compare the arguments passed to print_colored directly
        actual_calls = mock_print.call_args_list
        self.assertEqual(actual_calls, expected_calls)


    @patch(f"{SLOTS_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{SLOTS_FILE_PATH}.get_spin", return_value=["⬛", "⬛", "⬛"])
    @patch(f"{SLOTS_CLASS_PATH}.print_spin")
    @patch(f"{SLOTS_FILE_PATH}.get_payout", return_value=20.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_won(self, mock_print, mock_payout, mock_print_spin, mock_get_spin,
                          mock_money_input, mock_continue, mock_print_welcome):
        self.run_and_assert(mock_payout, mock_print_spin, mock_get_spin,
                            mock_money_input, mock_continue, mock_print_welcome)

        mock_print.assert_any_call("Congrats you won! $20.0 has been added to your account!", ANSI_COLORS.GREEN)


    @patch(f"{SLOTS_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, False])
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{SLOTS_FILE_PATH}.get_spin", return_value=["⬛", "⬛", "🍒"])
    @patch(f"{SLOTS_CLASS_PATH}.print_spin")
    @patch(f"{SLOTS_FILE_PATH}.get_payout", return_value=0.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_once_loss(self, mock_print, mock_payout, mock_print_spin, mock_get_spin,
                          mock_money_input, mock_continue, mock_print_welcome):
        self.run_and_assert(mock_payout, mock_print_spin, mock_get_spin,
                            mock_money_input, mock_continue, mock_print_welcome)

        mock_print.assert_any_call("Sorry, you lost")

    @patch(f"{SLOTS_CLASS_PATH}.print_welcome_message")
    @patch(f"{GAME_CLASS_PATH}.get_continue_input", side_effect=[True, True, False])
    @patch(f"{IOCONSOLE_PATH}.get_monetary_input", return_value=10.0)
    @patch(f"{SLOTS_FILE_PATH}.get_spin", side_effect=[["⬛", "⬛", "🍒"], ["⬛", "🍒", "🍒"]])
    @patch(f"{SLOTS_CLASS_PATH}.print_spin")
    @patch(f"{SLOTS_FILE_PATH}.get_payout", return_value=0.0)
    @patch(f"{IOCONSOLE_PATH}.print_colored")
    def test_run_twice(self, mock_print, mock_payout, mock_print_spin, mock_get_spin,
                           mock_money_input, mock_continue, mock_print_welcome):
        self.game.run()

        expected_call_count = 2

        self.assertEqual(expected_call_count, mock_print_spin.call_count)
        self.assertEqual(expected_call_count, mock_payout.call_count)
        self.assertEqual(expected_call_count, mock_get_spin.call_count)
        self.assertEqual(expected_call_count, mock_money_input.call_count)
        self.assertEqual(expected_call_count + 1, mock_continue.call_count)
        self.assertEqual(expected_call_count - 1, mock_print_welcome.call_count)

        mock_print.assert_any_call("Sorry, you lost")

    @patch(f"{SLOTS_FILE_PATH}.os.remove")
    @patch(f"{SLOTS_FILE_PATH}.os.path.exists", return_value=True)
    @patch(f"{SLOTS_CLASS_PATH}.run")
    def test_main(self, mock_run, mock_exists, mock_remove):
        main()

        mock_run.assert_called_once()
        mock_exists.assert_called_once_with("casino.db")
        mock_remove.assert_called_once_with("casino.db")
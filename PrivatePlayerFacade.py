from PlayerFacade import PlayerFacade
from InventoryPanel import InventoryPanel
from InventoryButtonPanel import InventoryButtonPanel
from SubmitButton import SubmitButton
from CurrentTradePhase import CurrentTradePhase

import pygame


class PrivatePlayerFacade(PlayerFacade):
    game_piece_icons = {
        "road": "./res/icons/roadIcon.png",
        "settlement": "./res/icons/settlementIcon.png",
        "city": "./res/icons/cityIcon.png"
    }
    development_card_icons = {
        "victory": "./res/icons/victoryIcon.png",
        "knight": "./res/icons/knightIcon.png",
        "monopoly": "./res/icons/monopolyIcon.png",
        "year_of_plenty": "./res/icons/yearOfPlentyIcon.png",
        "road_building": "./res/icons/roadBuildingIcon.png",
        "face_down": "./res/icons/genericCardIcon.png",
    }

    game_piece_icon_order = [
        game_piece_icons.get("road"),
        game_piece_icons.get("settlement"),
        game_piece_icons.get("city")]
    development_card_icon_order = [
        development_card_icons.get("victory"),
        development_card_icons.get("knight"),
        development_card_icons.get("monopoly"),
        development_card_icons.get("year_of_plenty"),
        development_card_icons.get("road_building")]

    def __init__(self, player, center, screen):
        super().__init__(player, center, screen)
        self.current_trading_phase = CurrentTradePhase.NONE.value
        self.resource_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 50),
            self.player.resource_bank.resources, self.resource_icon_order,
            self.INVENTORY_ICON_SIZE)
        self.resource_incrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 35),
            len(self.resource_icon_order), "up")
        self.resource_decrementers = InventoryButtonPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 80),
            len(self.resource_icon_order), "down")
        self.game_piece_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 150),
            self.player.game_piece_bank.game_pieces,
            self.game_piece_icon_order, self.INVENTORY_ICON_SIZE)
        '''TO-DO: Give development card bank as parameter 
        once Development card bank is implemented.'''
        self.development_card_panel = InventoryPanel(
            self.screen,
            (self.screen.get_width()*0.8 + 2, self.center[1] + 175),
            [0, 0, 0, 0, 0],
            self.development_card_icon_order, self.CARD_ICON_SIZE)
        self.resource_submit_button = SubmitButton(
            self.screen, (int(self.screen.get_width()*0.9), 115), "Submit")

    def begin_maritime_trade(self):
        self.resource_submit_button.enabled = True
        self.resource_submit_button.draw()
        self.advance_maritime_trade()

    def advance_maritime_trade(self):
        if self.current_trading_phase < len(CurrentTradePhase):
            self.current_trading_phase += 1
            self.player.set_resources_before_starting_trade_phase()
        else:
            self.current_trading_phase = CurrentTradePhase.NONE.value
            for button in self.resource_decrementers.buttons:
                if button.enabled:
                    button.enabled = False
            self.resource_submit_button.enabled = False
            self.resource_submit_button.draw()
        if self.current_trading_phase == CurrentTradePhase.DEPOSIT.value:
            self.prepare_buttons_for_maritime_deposit()
        elif self.current_trading_phase == CurrentTradePhase.WITHDRAW.value:
            self.prepare_buttons_for_maritime_withdraw()

    def prepare_buttons_for_maritime_deposit(self):
        for resource, trade_rate, button in zip(
                self.player.resource_bank.resources,
                self.player.trade_rates,
                self.resource_decrementers.buttons):
            if resource >= trade_rate:
                button.enabled = True
        self.resource_incrementers.draw()

    def prepare_buttons_for_maritime_withdraw(self):
        for resource, trade_rate, increment_button, decrement_button in zip(
                self.player.resource_bank.resources,
                self.player.trade_rates,
                self.resource_incrementers.buttons,
                self.resource_decrementers.buttons):
            if self.player.maritime_trade_points > 0:
                increment_button.enabled = True
            if decrement_button.enabled:
                decrement_button.enabled = False
        if self.player.maritime_trade_points > 0:
            self.resource_submit_button.enabled = False
            self.resource_submit_button.draw()
        self.resource_incrementers.draw()
        self.resource_decrementers.draw()

    def click_increment_for_maritime_trade(self, mouse_pos):
        resource = self.resource_incrementers.toggle_button_in_boundary(
            mouse_pos)
        if resource is not None:
            self.player.maritime_trade_points -= 1
            if self.current_trading_phase == CurrentTradePhase.DEPOSIT.value:
                self.player.resource_bank.deposit_resource(
                    resource, self.player.trade_rates[resource])
                self.player.resource_bank.validate_transaction()
                self.draw()
                self.handle_incrementers_during_maritime_deposit(resource)
            elif (self.current_trading_phase ==
                    CurrentTradePhase.WITHDRAW.value):
                self.player.resource_bank.deposit_resource(resource, 1)
                self.player.resource_bank.validate_transaction()
                self.draw()
                self.handle_incrementers_during_maritime_withdraw(resource)

    def click_decrement_for_maritime_trade(self, mouse_pos):
        resource = self.resource_decrementers.toggle_button_in_boundary(
            mouse_pos)
        if resource is not None:
            self.player.maritime_trade_points += 1
            if self.current_trading_phase == CurrentTradePhase.DEPOSIT.value:
                self.player.resource_bank.withdraw_resource(
                    resource, self.player.trade_rates[resource])
                self.player.resource_bank.validate_transaction()
                self.draw()
                self.handle_decrementers_during_maritime_deposit(resource)
            elif (self.current_trading_phase ==
                    CurrentTradePhase.WITHDRAW.value):
                self.player.resource_bank.withdraw_resource(resource, 1)
                self.player.resource_bank.validate_transaction()
                self.draw()
                self.handle_decrementers_during_maritime_withdraw(resource)

    def handle_incrementers_during_maritime_deposit(self, resource):
        self.resource_decrementers.buttons[resource].enabled = True
        self.resource_decrementers.draw()
        # The current resources and resources recorded at beginning of the
        # trade phase is always identical due to incrementing and
        # decrementing values being the resource's trade rate.
        if (self.player.resource_bank.resources[resource] ==
                self.player.resources_at_start_of_trade_phase[resource]):
            self.resource_incrementers.buttons[resource].enabled = False
            self.resource_incrementers.draw()

    def handle_decrementers_during_maritime_deposit(self, resource):
        self.resource_incrementers.buttons[resource].enabled = True
        self.resource_incrementers.draw()
        # Cannot deposit anymore resources if less than respective trade rate.
        if (self.player.resource_bank.resources[resource] <
                self.player.trade_rates[resource]):
            self.resource_decrementers.buttons[resource].enabled = False
            self.resource_decrementers.draw()

    def handle_incrementers_during_maritime_withdraw(self, resource):
        self.resource_decrementers.buttons[resource].enabled = True
        self.resource_decrementers.draw()
        # Revoke ability to increment resources if player collects the
        # amount allotted to him/her.
        if self.player.maritime_trade_points == 0:
            self.resource_submit_button.enabled = True
            self.resource_submit_button.draw()
            for button in self.resource_incrementers.buttons:
                button.enabled = False
            self.resource_incrementers.draw()

    def handle_decrementers_during_maritime_withdraw(self, resource):
        self.resource_decrementers.buttons[resource].enabled = True
        self.resource_decrementers.draw()
        # Will never be less than since all values start equal to the
        # values recorded before the trade phase.
        if (self.player.resource_bank.resources[resource] ==
                self.player.resources_at_start_of_trade_phase[resource]):
            self.resource_decrementers.buttons[resource].enabled = False
            self.resource_decrementers.draw()
        # Grant ability to increment resources if player has less than
        # the amount allotted to him/her.
        if self.player.maritime_trade_points > 0:
            self.resource_submit_button.enabled = False
            self.resource_submit_button.draw()
            for button in self.resource_incrementers.buttons:
                button.enabled = True
            self.resource_incrementers.draw()

    def draw(self):
        pygame.draw.rect(
            self.screen, (228, 205, 180),
            ((self.screen.get_width()*0.8, self.center[1]),
             (self.screen.get_width()*0.2, self.screen.get_height()*0.5)), 0)
        self.render_text(
            self.player.retrieve_player_name(),
            [self.screen.get_width()*0.8, self.center[1]])

        self.resource_incrementers.draw()
        self.resource_decrementers.draw()
        self.resource_panel.draw()
        self.game_piece_panel.draw()
        self.development_card_panel.draw()
        self.resource_submit_button.draw()

    def get_player(self):
        return self.player

    def get_maritime_trade_points(self):
        return self.player.maritime_trade_points

    def set_next_player(self, player):
        self.player = player
        self.resource_panel.update(player.resource_bank.resources)
        self.game_piece_panel.update(player.game_piece_bank.game_pieces)

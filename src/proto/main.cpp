#include <iostream>

#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <Thor/Input.hpp>

#include <proto/cannonball.hpp>
#include <proto/sea.hpp>
#include <proto/ship.hpp>

enum class Action {
	Move, Stop, Left, Right, Shoot
};

int main() {
	sf::RenderWindow window{{640u, 480u}, "Seegurke prototype"};
	sf::Texture cannonball_tex, water_tex, ship_tex;
	cannonball_tex.loadFromFile("cannonball.png");
	water_tex.loadFromFile("water.png");
	ship_tex.loadFromFile("ship.png");
	
	sf::View view;
	view.setSize({640u, 480u});
	view.setViewport({0.f, 0.f, 1.f, 1.f});
	
	proto::CannonballSystem balls{cannonball_tex};
	proto::Sea sea{water_tex};
	proto::Ship player{balls, {384u, 384u}, ship_tex};
	proto::Ship enemy{balls, {640u, 384}, ship_tex};
	enemy.cannonball_distance = 200.f;
	enemy.move();
	auto ai_delay = sf::Time::Zero;
	
	thor::ActionMap<Action> actions;
	actions[Action::Move]	= thor::Action(sf::Keyboard::W);
	actions[Action::Stop]	= thor::Action(sf::Keyboard::S);
	actions[Action::Left]	= thor::Action(sf::Keyboard::A);
	actions[Action::Right]	= thor::Action(sf::Keyboard::D);
	actions[Action::Shoot]	= thor::Action(sf::Keyboard::Space);
	
	thor::ActionMap<Action>::CallbackSystem system;
	system.connect0(Action::Move, [&]() {
		player.move();
	});
	system.connect0(Action::Stop, [&]() {
		player.stop();
	});
	system.connect0(Action::Left, [&]() {
		player.rotate(-1.f);
	});
	system.connect0(Action::Right, [&]() {
		player.rotate(1.f);
	});
	system.connect0(Action::Shoot, [&]() {
		player.shoot();
	});
	
	sf::Clock clock;
	window.setFramerateLimit(60u);
	while (window.isOpen()) {
		sf::Event event;
		while (window.pollEvent(event)) {
			if (event.type == sf::Event::Closed) {
				window.close();
			}
		}
		
		actions.invokeCallbacks(system, &window);
		
		auto elapsed = clock.restart();
		ai_delay -= elapsed;
		if (ai_delay <= sf::Time::Zero) {
			ai_delay = sf::milliseconds(2500);
			enemy.shoot();
		}
		enemy.rotate(-1.f);
		
		player.update(elapsed);
		enemy.update(elapsed);
		balls.update(elapsed);
		
		view.setCenter(player.getPosition());
		
		window.clear(sf::Color::Black);
		window.setView(view);
		
		window.draw(sea);
		window.draw(player);
		window.draw(enemy);
		window.draw(balls);
		
		window.display();
	}
}

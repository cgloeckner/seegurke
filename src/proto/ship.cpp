#include <proto/ship.hpp>
#include <iostream>

namespace proto {

Ship::Ship(CannonballSystem& system, sf::Vector2f position, sf::Texture const & tex)
	: sf::Drawable{}
	, system{system}
	, position{position}
	, rotation{0.f, -1.f}
	, angle{0.f}
	, moving{false}
	, sprite{tex}
	, cooldown{sf::Time::Zero} {
	sprite.setOrigin(sf::Vector2f{tex.getSize()} / 2.f);
}

void Ship::draw(sf::RenderTarget& target, sf::RenderStates states) const {
	states.transform.translate(position);
	states.transform.rotate(angle);
	target.draw(sprite, states);
}

sf::Vector2f Ship::getPosition() const {
	return position;
}

void Ship::rotate(float delta) {
	this->delta = delta;
}

void Ship::move() {
	moving = true;
}

void Ship::stop() {
	moving = false;
}

void Ship::shoot() {
	if (cooldown == sf::Time::Zero) {
		cooldown = sf::milliseconds(750);
		system.create(position, angle + 90.f);
		system.create(position, angle - 90.f);
	}
}

void Ship::update(sf::Time elapsed) {
	cooldown -= elapsed;
	if (cooldown < sf::Time::Zero) {
		cooldown = sf::Time::Zero;
	}
	
	if (moving) {
		if (delta != 0.f) {
			angle += delta * elapsed.asSeconds() * 25.f;
			delta = 0.f;
			while (angle >= 360.f) {
				angle -= 360.f;
			}
			// update rotation vector
			sf::Transform t;
			t.rotate(angle);
			rotation = t.transformPoint({0.f, -1.f});
		}
		
		auto speed = elapsed.asSeconds() * 30.f;
		position += rotation * speed;
	}
}

} // ::proto

#include <proto/common.hpp>
#include <proto/ship.hpp>

namespace proto {

Ship::Ship(CannonballSystem& system, sf::Vector2f position, sf::Texture const & tex)
	: sf::Drawable{}
	, system{system}
	, position{position}
	, rotation{0.f, -1.f}
	, angle{0.f}
	, moving{false}
	, sprite{tex}
	, cooldown{sf::Time::Zero}
	, cannonball_distance{75.f} {
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
		cooldown = sf::seconds(SHIP_SHOOT_DELAY);
		system.create(position, angle + 90.f, cannonball_distance);
		system.create(position, angle - 90.f, cannonball_distance);
	}
}

void Ship::update(sf::Time elapsed) {
	cooldown -= elapsed;
	if (cooldown < sf::Time::Zero) {
		cooldown = sf::Time::Zero;
	}
	
	if (moving) {
		if (delta != 0.f) {
			angle += delta * elapsed.asSeconds() * SHIP_STEER_SPEED;
			delta = 0.f;
			while (angle >= 360.f) {
				angle -= 360.f;
			}
			// update rotation vector
			sf::Transform t;
			t.rotate(angle);
			rotation = t.transformPoint({0.f, -1.f});
		}
		
		auto speed = elapsed.asSeconds() * SHIP_MOVE_SPEED;
		position += rotation * speed;
	}
}

} // ::proto

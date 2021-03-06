#include <algorithm>

#include <proto/common.hpp>
#include <proto/cannonball.hpp>

namespace proto {

Cannonball::Cannonball()
	: id{0u}
	, sprite{}
	, speed{1.f}
	, min_dist{0.f}
	, distance{0.f}
	, direction{0, -1.f} {
}

CannonballSystem::CannonballSystem(sf::Texture const & tex)
	: sf::Drawable{}
	, tex{tex}
	, next_id{0u}
	, balls{} {
}

void CannonballSystem::draw(sf::RenderTarget& target, sf::RenderStates states) const {
	for (auto const & ball: balls) {
		target.draw(ball.sprite, states);
	}
}

std::size_t CannonballSystem::create(sf::Vector2f position, float angle, float distance) {
	balls.emplace_back();
	auto& ball = balls.back();
	
	ball.id = next_id++;
	ball.sprite.setTexture(tex);
	ball.sprite.setOrigin(sf::Vector2f{tex.getSize()} / 2.f);
	ball.sprite.setPosition(position);
	ball.sprite.setRotation(angle);
	
	sf::Transform t;
	t.rotate(angle);
	ball.direction = t.transformPoint({0.f, -1.f});
	ball.min_dist = distance;
	
	return ball.id;
}

void CannonballSystem::destroy(std::size_t id) {
	balls.remove_if([&id](Cannonball const & ball) {
		return id == ball.id;
	});
}

void CannonballSystem::update(sf::Time elapsed) {
	auto speed = elapsed.asSeconds() * CANNONBALL_MOVE_SPEED;
	
	// remove only if cannonball gets too slow
	balls.remove_if([&speed](Cannonball& ball) {
		auto delta = speed * ball.speed;
		ball.distance += delta;
		ball.sprite.move(ball.direction * delta);
		if (ball.distance <= ball.min_dist * CANNONBALL_RISE_RATIO) {
			// make it rise
			ball.sprite.scale(CANNONBALL_RISE_SCALE, CANNONBALL_RISE_SCALE);
		} else if (ball.distance >= ball.min_dist) {
			// make it fall
			ball.sprite.scale(CANNONBALL_FALL_SCALE, CANNONBALL_FALL_SCALE);
			// slow it down
			ball.speed *= CANNONBALL_SLOWDOWN_SPEED;
		}
		return ball.speed < CANNONBALL_MIN_SPEED;
	});
}

} // ::proto

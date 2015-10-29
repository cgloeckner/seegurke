#include <algorithm>

#include <proto/cannonball.hpp>

namespace proto {

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

std::size_t CannonballSystem::create(sf::Vector2f position, float angle) {
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
	
	return ball.id;
}

void CannonballSystem::destroy(std::size_t id) {
	std::remove_if(balls.begin(), balls.end(), [&](Cannonball const & ball) {
		return id == ball.id;
	});
}

void CannonballSystem::update(sf::Time elapsed) {
	auto speed = elapsed.asSeconds() * 100.f;
	for (auto& ball: balls) {
		auto delta = ball.direction * speed;
		ball.sprite.move(delta);
	}
}

} // ::proto

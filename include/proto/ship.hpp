#pragma once
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>

#include <proto/cannonball.hpp>

namespace proto {

class Ship
	: public sf::Drawable {
	private:
		CannonballSystem& system;
		
		sf::Vector2f position, rotation;
		float angle, delta;
		bool moving;
		sf::Sprite sprite;
		sf::Time cooldown;
		
		void draw(sf::RenderTarget& target, sf::RenderStates states) const override;
		
	public:
		float cannonball_distance;
		
		Ship(CannonballSystem& system, sf::Vector2f position, sf::Texture const & tex);
		
		sf::Vector2f getPosition() const;
		
		void rotate(float delta);
		void move();
		void stop();
		void shoot();
		void update(sf::Time elapsed);
};

} // ::proto

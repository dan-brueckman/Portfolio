USE sakila 

-- 1a. Display the first and last names of all actors from the table actor.
SELECT first_name, last_name 
FROM actor;

-- 1b. Display the first and last name of each actor in a single column in upper case letters. Name the column Actor Name.
SELECT concat(first_name, ' ', last_name) AS 'Actor_Name'
FROM actor;

-- 2a. You need to find the ID number, first name, and last name of an actor, of whom you know only the first name, "Joe." What is one query would you use to obtain this information?
SELECT actor_id, first_name, last_name
FROM actor
WHERE first_name = 'Joe';

-- 2b. Find all actors whose last name contain the letters GEN:
SELECT first_name, last_name
FROM actor
WHERE last_name LIKE '%gen%';

-- 2c. Find all actors whose last names contain the letters LI. This time, order the rows by last name and first name, in that order:
SELECT last_name, first_name
FROM actor
WHERE last_name LIKE '%li%';

-- 2d. Using IN, display the country_id and country columns of the following countries: Afghanistan, Bangladesh, and China:
SELECT country_id, country
FROM country
WHERE country IN('Afghanistan', 'Bangladesh', 'China');

-- 3a. Add a middle_name column to the table actor. Position it between first_name and last_name. Hint: you will need to specify the data type.
ALTER TABLE actor
ADD middle_name VARCHAR(50) AFTER first_name;

-- 3b. You realize that some of these actors have tremendously long last names. Change the data type of the middle_name column to blobs.
ALTER TABLE actor
Modify middle_name blob(50);

-- 3c. Now delete the middle_name column.
ALTER TABLE actor
DROP COLUMN middle_name;

-- 4a. List the last names of actors, as well as how many actors have that last name.
select distinct last_name, count(last_name) as CountOf 
from actor 
group by last_name;

-- 4b. List last names of actors and the number of actors who have that last name, but only for names that are shared by at least two actors

select distinct last_name, count(last_name) as CountOf 
from actor
group by last_name
having count(last_name) >=2;

-- 4c. Oh, no! The actor HARPO WILLIAMS was accidentally entered in the actor table as GROUCHO WILLIAMS, the name of Harpo's second cousin's husband's yoga teacher. Write a query to fix the record.
UPDATE actor
set first_name = 'HARPO' 
where first_name = 'GROUCHO'
and last_name = 'WILLIAMS';

-- 4d. Perhaps we were too hasty in changing GROUCHO to HARPO. It turns out that GROUCHO was the correct name after all! In a single query, if the first name of the actor is currently HARPO, change it to GROUCHO. Otherwise, change the first name to MUCHO GROUCHO, as that is exactly what the actor will be with the grievous error. BE CAREFUL NOT TO CHANGE THE FIRST NAME OF EVERY ACTOR TO MUCHO GROUCHO, HOWEVER! (Hint: update the record using a unique identifier.)

update actor
set first_name = case when first_name = 'HARPO' then 'GROUCHO' else 'MUCHO' 
END
where actor_id = 172;

-- 5a. You cannot locate the schema of the address table. Which query would you use to re-create it?
 SHOW CREATE TABLE address;
 
-- 6a. Use JOIN to display the first and last names, as well as the address, of each staff member. Use the tables staff and address:

select s.first_name, s.last_name, a.address
from staff as s
inner join address as a
on s.address_id = a.address_id;

-- 6b. Use JOIN to display the total amount rung up by each staff member in August of 2005. Use tables staff and payment.

select s.first_name, s.last_name, sum(p.amount) as sum_of
from staff as s
inner join payment as p
on p.staff_id = s.staff_id
where p.payment_date like '2005-08%'
group by s.last_name;

-- 6c. List each film and the number of actors who are listed for that film. Use tables film_actor and film. Use inner join.

select f.title, count(fa.actor_id) as actor_count
from film as f
inner join film_actor as fa
on f.film_id = fa.film_id
group by f.title;

-- 6d. How many copies of the film Hunchback Impossible exist in the inventory system?

select f.title, count(i.inventory_id) as copies
from film as f
inner join inventory as i
on f.film_id = i.film_id
where f.title = 'Hunchback Impossible';

-- 6e. Using the tables payment and customer and the JOIN command, list the total paid by each customer. List the customers alphabetically by last name:
 
 select c.first_name, c.last_name, sum(p.amount) as total_paid
 from customer as c
 inner join payment as p
 on c.customer_id = p.customer_id
 group by c.last_name 
order by c.last_name asc;
 
-- 7a. The music of Queen and Kris Kristofferson have seen an unlikely resurgence. As an unintended consequence, films starting with the letters K and Q have also soared in popularity. Use subqueries to display the titles of movies starting with the letters K and Q whose language is English.

SELECT title, language_id 
FROM film
WHERE film_id IN(
	SELECT film_id
    FROM film
    WHERE language_id = 1
    and film_id IN(
		select film_id
        from film
        where title like 'Q%' 
        or title like 'K%')
); 

-- 7b. Use subqueries to display all actors who appear in the film Alone Trip.

select first_name, last_name 
from actor
where actor_id in(
	select actor_id 
    from film_actor 
    where film_id in(
		select film_id
        from film
        where title = 'Alone Trip')
); 

-- 7c. You want to run an email marketing campaign in Canada, for which you will need the names and email addresses of all Canadian customers. Use joins to retrieve this information.

select c.first_name, c.last_name, c.email
from customer as c
inner join address as a
on c.address_id = a.address_id
inner join city 
on city.city_id = a.city_id
inner join country 
on city.country_id = country.country_id
where country.country_id = 20;
	
-- 7d. Sales have been lagging among young families, and you wish to target all family movies for a promotion. Identify all movies categorized as famiy films.

select title 
from film
where film_id in(
	select film_id
    from film_category
    where category_id = 8);

-- 7e. Display the most frequently rented movies in descending order.

select distinct(r.inventory_id), count(r.inventory_id) as Times_Rented, f.title
from rental as r
inner join inventory as i
on i.inventory_id = r.inventory_id
inner join film as f
on i.film_id = f.film_id
group by r.inventory_id
order by count(r.inventory_id) desc;

-- 7f. Write a query to display how much business, in dollars, each store brought in.

select sum(amount), s.store_id
from payment as p
inner join staff as s
on s.staff_id = p.staff_id
group by store_id;

-- 7g. Write a query to display for each store its store ID, city, and country.

select s.store_id, c.city, co.country
from store as s
inner join address as a
on s.address_id = a.address_id
inner join city as c
on a.city_id = c.city_id
inner join country as co
on c.country_id = co.country_id;

-- 7h. List the top five genres in gross revenue in descending order. (Hint: you may need to use the following tables: category, film_category, inventory, payment, and rental.)

select sum(amount), cat.name
from payment as p
inner join rental as r 
on p.rental_id = r.rental_id
inner join inventory as i 
on r.inventory_id = i.inventory_id
inner join film as f
on i.film_id = f.film_id
inner join film_category as fcat
on f.film_id = fcat.film_id
inner join category as cat
on fcat.category_id = cat.category_id
group by name
order by sum(amount) desc;

-- 8a. In your new role as an executive, you would like to have an easy way of viewing the Top five genres by gross revenue. Use the solution from the problem above to create a view. If you haven't solved 7h, you can substitute another query to create a view.

create view top_g_rev 
as select sum(amount), cat.name
from payment as p
inner join rental as r 
on p.rental_id = r.rental_id
inner join inventory as i 
on r.inventory_id = i.inventory_id
inner join film as f
on i.film_id = f.film_id
inner join film_category as fcat
on f.film_id = fcat.film_id
inner join category as cat
on fcat.category_id = cat.category_id
group by name
order by sum(amount) desc
limit 5; 

-- 8b. How would you display the view that you created in 8a?

select * from top_g_rev;

-- 8c. You find that you no longer need the view top_five_genres. Write a query to delete it.

drop view top_g_rev;


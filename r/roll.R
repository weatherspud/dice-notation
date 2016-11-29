classes = list(
  cleric = c(3, 3, 9, 3, 3, 3),
  druid = c(3, 3, 12, 3, 3, 15),
  fighter = c(9, 3, 3, 3, 7, 3),
  paladin = c(12, 9, 13, 3, 9, 17),
  ranger = c(13, 13, 14, 3, 14, 3),
  magic_user = c(3, 9, 3, 6, 3, 3),
  illusionist = c(3, 15, 3, 16, 3, 3),
  thief = c(3, 3, 3, 9, 3, 3),
  assassin = c(12, 11, 3, 12, 3, 3),
  monk = c(15, 3, 15, 15, 11, 3),
  bard = c(15, 12, 15, 15, 10, 15)
);

roll = function(num_rolls, num_faces, num_keep=NULL) {
  if (is.null(num_keep)) {
    num_keep = num_rolls; 
  }
  if (num_keep > num_rolls) {
    stop('num_keep cannot exceed num_rolls');
  }
  sum(rev(sort(floor(runif(num_rolls) * num_faces + 1)))[seq(1, num_keep)]);
}

roll_attributes = function(num_rolls, num_faces, num_keep, rearrange=FALSE,
  size_attribute_pool=6, num_attribute_rolls=1) {
  if (size_attribute_pool < 6) {
    stop('size_attribute_pool must be at least 6');
  }
  if (rearrange == FALSE & size_attribute_pool > 6) {
    stop('if size_attribute_pool > 6, then rearrange must be TRUE');
  }
  attrs = rep(NA, size_attribute_pool);
  for (i in 1:size_attribute_pool) {
    max_attr = 0;
    for (j in 1:num_attribute_rolls) {
      max_attr = max(max_attr, roll(num_rolls, num_faces, num_keep));
    }
    attrs[i] = max_attr;
  }
  if (rearrange) {
    attrs = rev(sort(attrs)); 
  }
  attrs[seq(1, 6)];
}

roll_character = function(min_attributes, num_rolls, num_faces, num_keep,
  rearrange=FALSE, size_attribute_pool=6, num_attribute_rolls=1, num_character_rolls=1) {
  if (length(min_attributes) != 6) {
    stop('min_attributes must be length 6'); 
  }
  if (rearrange) {
    min_attrs = rev(sort(min_attributes)); 
  }
  else {
    min_attrs = min_attributes;
  }
  for (i in 1:num_character_rolls) {
    attrs = roll_attributes(num_rolls, num_faces, num_keep, rearrange,
      size_attribute_pool, num_attribute_rolls);
    if (all(attrs >= min_attrs)) {
      return(TRUE);
    }
  }
  FALSE;
}

simulate_class = function(times, min_attributes, num_rolls, num_faces, num_keep,
  rearrange=TRUE, size_attribute_pool=6, num_attribute_rolls=1, num_character_rolls=1) {
  success = 0;
  for (i in 1:times) {
    if (roll_character(min_attributes, num_rolls, num_faces, num_keep, rearrange,
      size_attribute_pool, num_attribute_rolls, num_character_rolls)) {
     success = success + 1; 
    }
  }
  100.0 * success / times;
}

simulate_classes = function(times, num_rolls, num_faces, num_keep, rearrange=FALSE,
  size_attribute_pool=6, num_attribute_rolls=1, num_character_rolls=1) {
  for (cls in sort(names(classes))) {
    cat(paste(cls, ': ', sep=''));
    cat(toString(simulate_class(times, classes[[cls]], num_rolls, num_faces, num_keep,
      rearrange, size_attribute_pool, num_attribute_rolls, num_character_rolls)));
    cat('\n');
  }
}

cat('METHOD I\n');
simulate_classes(10000, 4, 6, 3, rearrange=TRUE);

cat('METHOD II\n');
simulate_classes(10000, 3, 6, 3, rearrange=TRUE, size_attribute_pool=12);

cat('METHOD III\n');
simulate_classes(10000, 3, 6, 3, num_attribute_rolls=6);

cat('METHOD IV\n');
simulate_classes(10000, 3, 6, 3, num_character_rolls=12);

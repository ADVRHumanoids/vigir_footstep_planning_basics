#include <vigir_footstep_planning_plugins/collision_check_plugin.h>

namespace vigir_footstep_planning
{
CollisionCheckPlugin::CollisionCheckPlugin(const std::string& name)
  : vigir_pluginlib::Plugin(name)
  , collision_check_flag_(0)
{
}

bool CollisionCheckPlugin::initialize(ros::NodeHandle& nh, const vigir_generic_params::ParameterSet& params)
{
  if (!vigir_pluginlib::Plugin::initialize(nh, params))
    return false;

  getPluginParam("collision_check_flag", (int&)collision_check_flag_, -1, true);

  return true;
}

void CollisionCheckPlugin::loadParams(const vigir_generic_params::ParameterSet& params)
{
  Plugin::loadParams(params);

  // check if
  unsigned int collision_check_mask;
  params.getParam("collision_check/collision_check_mask", (int&)collision_check_mask);
  collision_check_enabled_ = this->collision_check_flag_ & collision_check_mask;
}

void CollisionCheckPlugin::reset()
{
}

bool CollisionCheckPlugin::isUnique() const
{
  return false;
}

bool CollisionCheckPlugin::isCollisionCheckAvailable() const
{
  return collision_check_enabled_;
}
}
